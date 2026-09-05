from __future__ import annotations

import ctypes
import json
import math
import os
import platform
import re
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from threading import RLock
from typing import Any

from .exceptions import THSDKError


_COMPONENT_LAYOUT = {
    "Darwin": ("darwin", "hq.dylib"),
    "Linux": ("linux", "hq.so"),
    "Windows": ("windows", "hq.dll"),
}

_ABI_VERSION = "2.0.0"
_MAX_REQUEST_BYTES = 1 << 20
_MAX_METHOD_BYTES = 128
_MAX_JSON_DEPTH = 64
_MAX_CALL_TIMEOUT_MS = 600_000
_JSON_FIELD_NAME = re.compile(r"^[a-z0-9_]+$")


def _validate_json_value(value: Any, *, depth: int = 0) -> None:
    """Apply the native ABI's JSON document rules before crossing ctypes."""

    if depth > _MAX_JSON_DEPTH:
        raise THSDKError("THSDK 请求的 JSON 嵌套超过 64 层")
    if isinstance(value, Mapping):
        for key, item in value.items():
            if not isinstance(key, str) or _JSON_FIELD_NAME.fullmatch(key) is None:
                raise THSDKError("THSDK 请求字段必须使用 ASCII 小写 snake_case")
            _validate_json_value(item, depth=depth + 1)
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for item in value:
            _validate_json_value(item, depth=depth + 1)
        return
    if isinstance(value, float) and not math.isfinite(value):
        raise THSDKError("THSDK 请求不能包含 NaN 或 Infinity")
    if value is None or isinstance(value, (str, int, float, bool)):
        return
    raise THSDKError(f"THSDK 请求包含不可序列化的值类型: {type(value).__name__}")


class _RuntimeBridge:
    """Private request bridge used by the process-local client."""

    def __init__(self, component_path: str | os.PathLike[str] | None = None):
        self.component_path = Path(component_path or self._resolve_component()).expanduser().resolve()
        if not self.component_path.is_file():
            raise THSDKError("未找到适用于当前环境的 THSDK 运行组件，请重新安装匹配的发行包")
        try:
            self._component = ctypes.CDLL(str(self.component_path))
        except OSError as exc:
            raise THSDKError("THSDK 运行组件加载失败，请确认安装包与当前环境匹配") from exc

        self._lock = RLock()
        if not hasattr(self._component, "CallAlloc") or not hasattr(self._component, "FreeResult"):
            raise THSDKError("THSDK 运行组件版本过旧，请重新安装")
        self._component.CallAlloc.argtypes = [ctypes.c_char_p]
        self._component.CallAlloc.restype = ctypes.c_void_p
        self._component.FreeResult.argtypes = [ctypes.c_void_p]
        self._component.FreeResult.restype = None

        version = self._handshake_call("version")
        runtime_version = (version.get("data") or {}).get("abi_version") if version.get("ok") else None
        if runtime_version != _ABI_VERSION:
            raise THSDKError("THSDK 运行组件版本不兼容，请重新安装")

        # ABI 2.0.0 existed before strict request decoding. Probe behavior rather
        # than trusting the unchanged version string so an older component cannot
        # silently accept misspelled or unknown request fields.
        strict_probe = self._handshake_call(
            "version",
            {"thsdk_protocol_probe": True},
        )
        strict_error = strict_probe.get("error") or {}
        if strict_probe.get("ok") or strict_error.get("code") != "invalid_request":
            raise THSDKError("THSDK 运行组件请求协议过旧，请安装最新版运行组件")

        from ._method_manifest import NATIVE_METHOD_NAMES

        methods = self._handshake_call("methods")
        runtime_methods = methods.get("data") if methods.get("ok") else None
        if runtime_methods != sorted(NATIVE_METHOD_NAMES):
            raise THSDKError("THSDK 运行组件方法清单不兼容，请重新安装")

    def _handshake_call(self, method: str, params: Any = None) -> dict[str, Any]:
        """Retry only the native pre-execution rate-limit response during startup."""

        response = self.call(method, params)
        error = response.get("error") or {}
        if not isinstance(error, dict):
            return response
        retry_after_ms = error.get("retry_after_ms")
        if (
            error.get("code") == "rate_limited"
            and isinstance(retry_after_ms, int)
            and not isinstance(retry_after_ms, bool)
            and 0 < retry_after_ms <= 1_000
        ):
            time.sleep(retry_after_ms / 1000)
            return self.call(method, params)
        return response

    @staticmethod
    def _resolve_component() -> Path:
        override = os.getenv("THSDK_RUNTIME_PATH")
        if override:
            return Path(override)

        layout = _COMPONENT_LAYOUT.get(platform.system())
        machine = platform.machine().lower()
        if layout is None or machine not in {"arm64", "aarch64", "x86_64", "amd64"}:
            raise THSDKError("当前环境暂不受此安装包支持，请安装匹配的 THSDK 发行包")
        architecture = "arm64" if machine in {"arm64", "aarch64"} else "amd64"
        family, filename = layout
        return Path(__file__).resolve().parent / "libs" / family / architecture / filename

    def call(self, method: str, params: Any = None, *, timeout_ms: int | None = None) -> dict[str, Any]:
        if not isinstance(method, str) or not method or method != method.strip():
            raise THSDKError("THSDK method 必须是非空规范名称")
        if (
            len(method.encode("utf-8")) > _MAX_METHOD_BYTES
            or _JSON_FIELD_NAME.fullmatch(method) is None
        ):
            raise THSDKError("THSDK method 必须是不超过 128 字节的 ASCII 小写 snake_case")
        if timeout_ms is not None:
            if (
                isinstance(timeout_ms, bool)
                or not isinstance(timeout_ms, int)
                or timeout_ms < 0
                or timeout_ms > _MAX_CALL_TIMEOUT_MS
            ):
                raise THSDKError("timeout_ms 必须是 0（默认）或 1 到 600000 之间的整数")

        request: dict[str, Any] = {"method": method}
        if params is not None:
            request["params"] = params
        if timeout_ms is not None:
            request["timeout_ms"] = timeout_ms
        _validate_json_value(request)
        try:
            encoded = json.dumps(
                request,
                ensure_ascii=False,
                allow_nan=False,
                separators=(",", ":"),
            ).encode("utf-8")
        except (TypeError, ValueError) as exc:
            raise THSDKError("THSDK 请求无法编码为严格 JSON") from exc
        if len(encoded) > _MAX_REQUEST_BYTES:
            raise THSDKError("THSDK 请求超过 1 MiB 限制")

        with self._lock:
            raw = self._call_allocated(encoded)
        try:
            response = json.loads(raw)
        except (TypeError, ValueError) as exc:
            raise THSDKError("THSDK 运行组件返回了无效数据") from exc
        if not isinstance(response, dict) or not isinstance(response.get("ok"), bool):
            raise THSDKError("THSDK 运行组件返回了不兼容的数据")
        return response

    def _call_allocated(self, encoded: bytes) -> str:
        pointer = self._component.CallAlloc(encoded)
        if not pointer:
            raise THSDKError("THSDK 运行组件未返回结果")
        try:
            return ctypes.string_at(pointer).decode("utf-8")
        finally:
            self._component.FreeResult(pointer)

from __future__ import annotations

import ctypes
import json
import os
import platform
from pathlib import Path
from threading import RLock
from typing import Any

from .exceptions import THSDKError


_COMPONENT_LAYOUT = {
    "Darwin": ("darwin", "hq.dylib"),
    "Linux": ("linux", "hq.so"),
    "Windows": ("windows", "hq.dll"),
}


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
        version = self.call("version")
        runtime_version = (version.get("data") or {}).get("abi_version") if version.get("ok") else None
        if runtime_version != "2.0.0":
            raise THSDKError("THSDK 运行组件版本不兼容，请重新安装")

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
        request: dict[str, Any] = {"method": method}
        if params is not None:
            request["params"] = params
        if timeout_ms is not None:
            request["timeout_ms"] = int(timeout_ms)
        encoded = json.dumps(request, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

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

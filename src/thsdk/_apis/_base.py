from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date, datetime
from enum import Enum
import math
import re
from typing import Any
from zoneinfo import ZoneInfo

from ..session import _get_client


ObjectParams = Mapping[str, Any]
SecurityInput = str | Mapping[str, Any]
BlockInput = int | Mapping[str, Any]


_SHANGHAI = ZoneInfo("Asia/Shanghai")
_MAX_TIMEOUT_SECONDS = 600
_JSON_FIELD_NAME = re.compile(r"^[a-z0-9_]+$")


def _timeout(value: float | None) -> float | None:
    if value is not None and (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value <= 0
        or value > _MAX_TIMEOUT_SECONDS
    ):
        raise ValueError("timeout 必须大于 0 且不超过 600 秒")
    return value


def _json_value(value: Any) -> Any:
    """Convert common Python containers and enums without changing field names."""

    if isinstance(value, Enum):
        return _json_value(value.value)
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=_SHANGHAI)
        return value.isoformat()
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time(), tzinfo=_SHANGHAI).isoformat()
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str) or _JSON_FIELD_NAME.fullmatch(key) is None:
                raise TypeError("请求字段必须使用 ASCII 小写 snake_case")
            if item is not None:
                result[key] = _json_value(item)
        return result
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    return value


def _normalize_block(value: BlockInput) -> dict[str, Any]:
    if isinstance(value, bool):
        raise TypeError("板块必须是 ID 或标准板块映射")
    if isinstance(value, int):
        if value <= 0:
            raise ValueError("板块 ID 必须大于 0")
        return {"id": value}
    if not isinstance(value, Mapping):
        raise TypeError("板块必须是 ID 或标准板块映射")
    return dict(value)


def _normalize_named_fields(
    fields: Mapping[str, Any],
    *,
    datetime_fields: frozenset[str],
) -> dict[str, Any]:
    payload = dict(fields)
    for key in ("security", "etf"):
        if key in payload:
            payload[key] = _normalize_security(payload[key])
    for key in ("securities", "exclude_securities"):
        if key in payload:
            value = payload[key]
            if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
                raise TypeError(f"{key} 必须是证券序列")
            payload[key] = [_normalize_security(item) for item in value]
    for key in ("market",):
        if key in payload:
            payload[key] = str(payload[key]).strip().upper()
    for key in ("markets",):
        if key in payload:
            value = payload[key]
            if isinstance(value, str):
                value = [item for item in value.replace(",", " ").split() if item]
            payload[key] = [str(item).strip().upper() for item in value]
    for key in ("block",):
        if key in payload:
            payload[key] = _normalize_block(payload[key])
    for key in ("blocks", "exclude_blocks"):
        if key in payload:
            value = payload[key]
            if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
                raise TypeError(f"{key} 必须是板块序列")
            payload[key] = [_normalize_block(item) for item in value]
    for key in datetime_fields:
        if key in payload:
            payload[key] = _json_value(payload[key])
    return _json_value(payload)


def _call_typed(
    method: str,
    params: ObjectParams | None,
    named_fields: Mapping[str, Any],
    *,
    required: tuple[str, ...],
    datetime_fields: tuple[str, ...] = (),
    timeout: float | None = None,
) -> Any:
    supplied = {key: value for key, value in named_fields.items() if value is not None}
    if params is not None:
        if supplied:
            raise TypeError("params 与关键字请求字段不能同时提供")
        if not isinstance(params, Mapping):
            raise TypeError("params 必须是映射对象")
        unknown = sorted(str(key) for key in params if key not in named_fields)
        if unknown:
            raise TypeError(f"未知请求字段: {', '.join(unknown)}")
        payload = _json_value(dict(params))
    else:
        missing = [name for name in required if name not in supplied]
        if missing:
            raise TypeError(f"缺少必填请求字段: {', '.join(missing)}")
        payload = _normalize_named_fields(
            supplied,
            datetime_fields=frozenset(datetime_fields),
        )
    return _get_client()._request(method, payload, timeout=_timeout(timeout))


def _call_none(method: str, *, timeout: float | None = None) -> Any:
    return _get_client()._request(method, timeout=_timeout(timeout))


def _call_string(
    method: str,
    value: str,
    *,
    argument: str,
    timeout: float | None = None,
) -> Any:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{argument} 必须是非空字符串")
    return _get_client()._request(method, value.strip(), timeout=_timeout(timeout))


def _normalize_security(value: SecurityInput) -> dict[str, str]:
    if isinstance(value, Mapping):
        code = str(value.get("code") or "").strip()
        market = str(value.get("market") or "").strip().upper()
    elif isinstance(value, str):
        full_code = value.strip()
        market, code = full_code[:4].upper(), full_code[4:]
    else:
        raise TypeError("证券必须是完整代码字符串或包含 code/market 的映射")
    if len(market) != 4 or not market.isalpha() or not code:
        raise ValueError("请使用完整证券代码，或包含 code 和四位 market 的映射")
    return {"code": code, "market": market}


def _call_securities(
    method: str,
    securities: Sequence[SecurityInput],
    *,
    timeout: float | None = None,
) -> Any:
    if isinstance(securities, (str, bytes)) or not isinstance(securities, Sequence):
        raise TypeError("securities 必须是证券序列")
    if not securities:
        raise ValueError("securities 不能为空")
    payload = [_normalize_security(item) for item in securities]
    return _get_client()._request(method, payload, timeout=_timeout(timeout))


__all__: list[str] = []

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Iterable, Sequence
from zoneinfo import ZoneInfo

from ._apis import *
from ._apis import __all__ as _native_api_all
from ._method_manifest import NativeMethodSpec, method_inventory
from .session import _get_client


_SHANGHAI = ZoneInfo("Asia/Shanghai")

_PERIODS = {
    "1m": 0x3001,
    "5m": 0x3005,
    "15m": 0x300F,
    "30m": 0x301E,
    "60m": 0x303C,
    "120m": 0x3078,
    "day": 0x4000,
    "daily": 0x4000,
    "1d": 0x4000,
    "week": 0x5001,
    "weekly": 0x5001,
    "month": 0x6001,
    "monthly": 0x6001,
    "quarter": 0x6003,
    "year": 0x7001,
}

_ADJUSTMENTS = {
    None: 0,
    "": 0,
    "none": 0,
    "pre": 1,
    "forward": 1,
    "post": 2,
    "backward": 2,
}


def auth(
    username: str | None = None,
    password: str | None = None,
    mac: str | None = None,
) -> bool:
    """按显式凭据、环境变量、已有会话、临时账户的顺序完成认证。"""
    return _get_client().auth(username, password, mac)


def auth_qrcode(
    *,
    timeout: float = 120,
    poll_interval: float = 1,
) -> bool:
    """优先恢复已有会话；需要时直接显示二维码和地址并等待扫码。"""
    return _get_client().auth_qrcode(timeout=timeout, poll_interval=poll_interval)


def logout() -> None:
    """退出当前账号并删除当前目录中可复用的会话文件。"""
    _get_client().logout()


def _request(method: str, params: Any = None, *, timeout: float | None = None) -> Any:
    return _get_client()._request(method, params, timeout=timeout)


def _security(value: str | dict[str, Any]) -> dict[str, str]:
    if isinstance(value, dict):
        code = str(value.get("code") or "").strip().upper()
        market = str(value.get("market") or "").strip().upper()
        if not code or len(market) != 4 or not market.isalpha():
            raise ValueError("security 字典必须包含 code 和四位 market")
        return {"code": code, "market": market}

    if not isinstance(value, str) or not value.strip():
        raise ValueError("证券代码必须是非空字符串")
    full_code = value.strip().upper()
    market, code = full_code[:4], full_code[4:]
    if len(market) != 4 or not market.isalpha() or not code:
        raise ValueError("请使用完整证券代码，例如 USHA600519 或 USZA300033")
    return {"code": code, "market": market}


def _securities(value: str | dict[str, Any] | Sequence[str | dict[str, Any]]) -> list[dict[str, str]]:
    if isinstance(value, (str, dict)):
        return [_security(value)]
    if not isinstance(value, Sequence) or not value:
        raise ValueError("证券代码不能为空")
    return [_security(item) for item in value]


def _market(value: str) -> str:
    market = str(value).strip().upper()
    if len(market) != 4 or not market.isalpha():
        raise ValueError("市场代码必须是四位字母，例如 USHA 或 USZA")
    return market


def _markets(value: str | Iterable[str] | None) -> list[str] | None:
    if value is None:
        return None
    if isinstance(value, str):
        values = [item for item in value.replace(",", " ").split() if item]
    else:
        values = list(value)
    if not values:
        return None
    return [_market(item) for item in values]


def _date_number(value: str | date | datetime | int | None) -> int | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return int(value.strftime("%Y%m%d"))
    if isinstance(value, date):
        return int(value.strftime("%Y%m%d"))
    if isinstance(value, int):
        text = str(value)
    else:
        text = str(value).strip().replace("-", "")
    if len(text) != 8 or not text.isdigit():
        raise ValueError("日期必须为 YYYY-MM-DD、YYYYMMDD、date 或 datetime")
    return int(text)


def _date_text(value: str | date | datetime | int | None) -> str:
    number = _date_number(value)
    return "0" if number is None else str(number)


def _datetime_text(value: str | date | datetime) -> str:
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, date):
        parsed = datetime.combine(value, datetime.min.time())
    else:
        text = str(value).strip().replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError as exc:
            raise ValueError("时间必须是 datetime、date 或 ISO 8601 字符串") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=_SHANGHAI)
    return parsed.isoformat()


def _frame(rows: Any, *, time_index: bool = False):
    try:
        import pandas as pd
    except ImportError as exc:
        raise ImportError("表格结果需要 pandas") from exc

    frame = pd.DataFrame(rows or [])
    if time_index and "time" in frame.columns:
        text = frame["time"].astype(str)
        if not frame.empty and text.str.fullmatch(r"\d{8}").all():
            frame["time"] = pd.to_datetime(text, format="%Y%m%d")
        frame = frame.set_index("time")
    return frame


def _identity_rows(rows: Any) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for item in rows or []:
        if not isinstance(item, dict):
            continue
        row = dict(item)
        security = row.pop("security", None)
        if isinstance(security, dict):
            code = str(security.get("code") or "")
            market = str(security.get("market") or "")
            row.setdefault("code", code)
            row.setdefault("market", market)
            row.setdefault("full_code", f"{market}{code}" if market and code else "")
        result.append(row)
    return result


def get_price(
    security: str | dict[str, Any],
    start_date: str | date | datetime | int | None = None,
    end_date: str | date | datetime | int | None = None,
    frequency: str = "daily",
    fields: Iterable[str] | None = None,
    fq: str | None = "pre",
    count: int | None = None,
):
    """查询一只证券的 K 线并返回 ``pandas.DataFrame``。"""
    period = _PERIODS.get(str(frequency).lower())
    if period is None:
        raise ValueError(f"不支持的 frequency: {frequency}")
    adjustment = _ADJUSTMENTS.get(None if fq is None else str(fq).lower())
    if adjustment is None:
        raise ValueError(f"不支持的 fq: {fq}")
    if count is not None and (start_date is not None or end_date is not None):
        raise ValueError("count 不能与 start_date/end_date 同时使用")
    if (start_date is None) != (end_date is None):
        raise ValueError("start_date 和 end_date 必须同时提供")
    if count is not None:
        if count <= 0:
            raise ValueError("count 必须大于 0")
        start, end = -int(count), 0
    elif start_date is not None:
        if str(frequency).lower().endswith("m"):
            raise ValueError("分钟 K 线的日期范围暂不支持；请改用 count")
        start = _date_number(start_date)
        end = _date_number(end_date)
    else:
        start, end = -1, 0

    rows = list_security_k_lines(
        security=_security(security),
        start=start,
        end=end,
        adjust=adjustment,
        period=period,
    )
    if count is not None and isinstance(rows, list):
        rows = rows[-int(count) :]
    frame = _frame(rows, time_index=True)
    if fields is not None:
        selected = [str(field) for field in fields]
        missing = [field for field in selected if field not in frame.columns]
        if missing:
            raise ValueError(f"返回结果缺少字段: {', '.join(missing)}")
        frame = frame[selected]
    return frame


def klines(
    ths_code: str | dict[str, Any],
    start_time: str | date | datetime | int | None = None,
    end_time: str | date | datetime | int | None = None,
    adjust: str = "",
    interval: str = "day",
    count: int | None = None,
):
    """使用传统参数名查询 K 线；返回 ``pandas.DataFrame``。"""
    if count is None and start_time is None and end_time is None:
        count = 100
    return get_price(
        ths_code,
        start_date=start_time,
        end_date=end_time,
        frequency=interval,
        fq=adjust,
        count=count,
    )


def intraday_data(ths_code: str | dict[str, Any], date: str | date | datetime | int | None = None):
    """查询指定交易日的分时走势；不传日期时查询当天。"""
    rows = list_security_intraday_bars(
        security=_security(ths_code),
        date=_date_text(date),
    )
    return _frame(rows)


def tick_level1(
    ths_code: str | dict[str, Any],
    count: int | None = 100,
    *,
    start_time: str | date | datetime | None = None,
    end_time: str | date | datetime | None = None,
):
    """查询普通逐笔成交，可按最近条数或明确时间范围读取。"""
    if count is not None and (start_time is not None or end_time is not None):
        raise ValueError("count 不能与 start_time/end_time 同时使用")
    if (start_time is None) != (end_time is None):
        raise ValueError("start_time 和 end_time 必须同时提供")
    if count is not None:
        if count <= 0:
            raise ValueError("count 必须大于 0")
        window = {"count": int(count)}
    elif start_time is not None and end_time is not None:
        window = {"start": _datetime_text(start_time), "end": _datetime_text(end_time)}
    else:
        raise ValueError("请提供 count，或同时提供 start_time 和 end_time")
    rows = list_security_ticks(security=_security(ths_code), window=window)
    if count is not None and isinstance(rows, list):
        rows = rows[-int(count) :]
    return _frame(rows)


def depth(ths_code: str | dict[str, Any] | Sequence[str | dict[str, Any]]):
    """查询一只或多只证券的五档盘口，按买卖方向和档位展开为表格。"""
    books = list_security_order_books(
        securities=_securities(ths_code),
        depth="5",
    )
    rows: list[dict[str, Any]] = []
    for book in books or []:
        security = book.get("security") or {}
        full_code = f"{security.get('market', '')}{security.get('code', '')}"
        for side_name, side in (("bid", book.get("bids")), ("ask", book.get("asks"))):
            for level, quote in enumerate(side or [], start=1):
                rows.append(
                    {
                        "full_code": full_code,
                        "side": side_name,
                        "level": level,
                        "price": quote.get("price"),
                        "volume": quote.get("volume"),
                    }
                )
    return _frame(rows)


def corporate_action(ths_code: str | dict[str, Any], count: int = 100):
    """查询最近的分红、送转、配股和除权除息记录。"""
    if count <= 0:
        raise ValueError("count 必须大于 0")
    rows = list_security_corporate_actions(
        security=_security(ths_code),
        start=-int(count),
        end=0,
        adjust=0,
        period=_PERIODS["day"],
    )
    if isinstance(rows, list):
        rows = rows[-int(count) :]
    return _frame(rows)


def search_symbols(pattern: str, market: str | None = None):
    """按代码、拼音或中文名称搜索证券。"""
    pattern = str(pattern).strip()
    if not pattern:
        raise ValueError("pattern 不能为空")
    params: dict[str, Any] = {"pattern": pattern}
    if market:
        params["market"] = _market(market)
    return _frame(_identity_rows(search_securities(params)))


def complete_ths_code(ths_code: str | Sequence[str]):
    """把一个或多个短代码解析为可用于行情查询的完整证券代码。"""
    if isinstance(ths_code, str):
        codes = [ths_code]
    else:
        codes = list(ths_code)
    codes = [str(code).strip().upper() for code in codes if str(code).strip()]
    if not codes:
        raise ValueError("ths_code 不能为空")
    return _frame(_identity_rows(resolve_securities(codes=codes)))


def wencai_nlp(condition: str, markets: str | Iterable[str] | None = None, limit: int = 100):
    """执行自然语言选股，并把动态字段展开为表格列。"""
    condition = str(condition).strip()
    if not condition:
        raise ValueError("condition 不能为空")
    if limit <= 0:
        raise ValueError("limit 必须大于 0")
    params: dict[str, Any] = {"query": condition, "limit": int(limit)}
    selected_markets = _markets(markets)
    if selected_markets:
        params["markets"] = selected_markets
    data = query_wencai(params) or {}
    field_names: dict[tuple[int, str], str] = {}
    for field in data.get("fields") or []:
        if not isinstance(field, dict):
            continue
        key = (int(field.get("index") or 0), str(field.get("timestamp") or ""))
        name = str(
            field.get("display_name")
            or field.get("show_name")
            or field.get("index_name")
            or field.get("query_key")
            or ""
        ).strip()
        if name:
            field_names[key] = name

    rows: list[dict[str, Any]] = []
    for item in data.get("rows") or []:
        security = item.get("security") or {}
        row: dict[str, Any] = {
            "full_code": item.get("full_code")
            or f"{security.get('market', '')}{security.get('code', '')}",
            "code": item.get("code") or security.get("code"),
            "market": item.get("market") or security.get("market"),
        }
        for cell in item.get("cells") or []:
            cell_name = str(cell.get("name") or "").strip()
            if cell_name == "code":
                continue
            key = (int(cell.get("key_index") or 0), str(cell.get("timestamp") or ""))
            name = field_names.get(key) or cell_name
            if name:
                row[name] = cell.get("value")
        rows.append(row)
    frame = _frame(rows)
    frame.attrs["query"] = data.get("query", condition)
    frame.attrs["fields"] = data.get("fields") or []
    return frame


def news(*, page: int = 1, page_size: int = 20, tag: str = ""):
    """查询 7x24 快讯；分页信息保存在返回表格的 ``attrs`` 中。"""
    if page <= 0 or page_size <= 0:
        raise ValueError("page 和 page_size 必须大于 0")
    data = list_news_flash_items(
        traversal="page",
        page=int(page),
        page_size=int(page_size),
        tag=str(tag).strip(),
    ) or {}
    frame = _frame(data.get("items"))
    frame.attrs.update({key: value for key, value in data.items() if key != "items"})
    return frame


def market_securities(market: str, *, start: int = 0, count: int = 100):
    """按市场列出证券；总数等分页信息保存在返回表格的 ``attrs`` 中。"""
    if start < 0 or count <= 0:
        raise ValueError("start 不能小于 0，count 必须大于 0")
    data = list_market_securities(
        market=_market(market),
        sort_begin=int(start),
        sort_count=int(count),
    ) or {}
    frame = _frame(_identity_rows(data.get("securities")))
    frame.attrs.update({key: value for key, value in data.items() if key != "securities"})
    return frame


def block_constituents(block: int | str, *, start: int = 0, count: int = 100):
    """按板块 ID 或名称查询成分证券。"""
    if start < 0 or count <= 0:
        raise ValueError("start 不能小于 0，count 必须大于 0")
    if isinstance(block, int):
        if block <= 0:
            raise ValueError("板块 ID 必须大于 0")
        identity = {"id": block}
    else:
        name = str(block).strip()
        if not name:
            raise ValueError("板块名称不能为空")
        identity = resolve_block(name=name)
    rows = list_block_constituents(
        block=identity,
        sort_begin=int(start),
        sort_count=int(count),
        sort_order="D",
    )
    return _frame(_identity_rows(rows))


_CONVENIENCE_API = [
    "auth",
    "auth_qrcode",
    "logout",
    "get_price",
    "klines",
    "intraday_data",
    "tick_level1",
    "depth",
    "corporate_action",
    "search_symbols",
    "complete_ths_code",
    "wencai_nlp",
    "news",
    "market_securities",
    "block_constituents",
]

# Canonical wrappers mirror every synchronous business method advertised by
# the bundled runtime. They intentionally keep the native JSON field names
# and return shapes; the convenience functions retain their DataFrame
# conversions and compatibility-oriented arguments.
__all__ = [
    *_CONVENIENCE_API,
    "NativeMethodSpec",
    "method_inventory",
    *_native_api_all,
]

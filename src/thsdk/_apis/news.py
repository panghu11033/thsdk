from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date, datetime
from typing import Any

from ._base import (
    BlockInput,
    ObjectParams,
    SecurityInput,
    _call_none,
    _call_securities,
    _call_string,
    _call_typed,
)


def analyze_security_limit_up(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    date: str | date | datetime | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``AnalyzeSecurityLimitUp``；请求 ``SecurityLimitUpAnalysisRequest``，返回 ``SecurityLimitUpAnalysisResult``。"""

    return _call_typed(
        "analyze_security_limit_up",
        params,
        {
            "security": security,
            "date": date,
        },
        required=("security",),
        datetime_fields=("date",),
        timeout=timeout,
    )


def get_security_price_limit_events(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    start_year: int | None = None,
    end_year: int | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``GetSecurityPriceLimitEvents``；请求 ``PriceLimitEventsRequest``，返回 ``PriceLimitEventsResult``。"""

    return _call_typed(
        "get_security_price_limit_events",
        params,
        {
            "security": security,
            "start_year": start_year,
            "end_year": end_year,
        },
        required=("security",),
        timeout=timeout,
    )


def get_security_short_term_highlights(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``GetSecurityShortTermHighlights``；请求 ``SecurityShortTermHighlightsRequest``，返回 ``SecurityShortTermHighlightsResult``。"""

    return _call_typed(
        "get_security_short_term_highlights",
        params,
        {
            "security": security,
        },
        required=("security",),
        timeout=timeout,
    )


def list_commodity_stock_linkage_news(
    params: ObjectParams | None = None,
    *,
    commodity_index: Mapping[str, Any] | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListCommodityStockLinkageNews``；请求 ``CommodityStockLinkageNewsRequest``，返回 ``CommodityStockLinkageNewsResult``。"""

    return _call_typed(
        "list_commodity_stock_linkage_news",
        params,
        {
            "commodity_index": commodity_index,
        },
        required=("commodity_index",),
        timeout=timeout,
    )


def list_hot_block_calendar_events(*, timeout: float | None = None) -> Any:
    """调用原生 ``ListHotBlockCalendarEvents``，返回 ``HotBlockCalendarResult``。"""

    return _call_none("list_hot_block_calendar_events", timeout=timeout)


def list_hot_event_news(
    params: ObjectParams | None = None,
    *,
    block: BlockInput | None = None,
    range: str | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListHotEventNews``；请求 ``HotEventNewsRequest``，返回 ``HotEventNewsResult``。"""

    return _call_typed(
        "list_hot_event_news",
        params,
        {
            "block": block,
            "range": range,
        },
        required=("block",),
        timeout=timeout,
    )


def list_market_call_auction_unusual_events(
    params: ObjectParams | None = None,
    *,
    market: str | None = None,
    trade_date: str | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListMarketCallAuctionUnusualEvents``；请求 ``CallAuctionUnusualEventsRequest``，返回 ``list[ShortTermEvent]``。"""

    return _call_typed(
        "list_market_call_auction_unusual_events",
        params,
        {
            "market": market,
            "trade_date": trade_date,
        },
        required=("market",),
        timeout=timeout,
    )


def list_market_change_events(*, timeout: float | None = None) -> Any:
    """调用原生 ``ListMarketChangeEvents``，返回 ``list[MarketChangeEvent]``。"""

    return _call_none("list_market_change_events", timeout=timeout)


def list_market_short_term_events(
    params: ObjectParams | None = None,
    *,
    market: str | None = None,
    mode: str | None = None,
    securities: Sequence[SecurityInput] | None = None,
    max_count: int | None = None,
    before_timestamp_micros: int | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListMarketShortTermEvents``；请求 ``MarketShortTermEventsRequest``，返回 ``list[ShortTermEvent]``。"""

    return _call_typed(
        "list_market_short_term_events",
        params,
        {
            "market": market,
            "mode": mode,
            "securities": securities,
            "max_count": max_count,
            "before_timestamp_micros": before_timestamp_micros,
        },
        required=("market", "mode"),
        timeout=timeout,
    )


def list_news_flash_items(
    params: ObjectParams | None = None,
    *,
    traversal: str | None = None,
    tag: str | None = None,
    tag_id: int | None = None,
    page: int | None = None,
    page_size: int | None = None,
    page_time: str | None = None,
    sequence: str | None = None,
    created_at: str | None = None,
    environment: str | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListNewsFlashItems``；请求 ``NewsFlashItemsRequest``，返回 ``NewsFlashItemsResult``。"""

    return _call_typed(
        "list_news_flash_items",
        params,
        {
            "traversal": traversal,
            "tag": tag,
            "tag_id": tag_id,
            "page": page,
            "page_size": page_size,
            "page_time": page_time,
            "sequence": sequence,
            "created_at": created_at,
            "environment": environment,
        },
        required=("traversal",),
        timeout=timeout,
    )


def list_news_items(
    params: ObjectParams | None = None,
    *,
    category: int | None = None,
    security: SecurityInput | None = None,
    market: str | None = None,
    traversal: Mapping[str, Any] | None = None,
    summary_mode: int | None = None,
    advertorial: bool | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListNewsItems``；请求 ``NewsItemsRequest``，返回 ``NewsItemsResult``。"""

    return _call_typed(
        "list_news_items",
        params,
        {
            "category": category,
            "security": security,
            "market": market,
            "traversal": traversal,
            "summary_mode": summary_mode,
            "advertorial": advertorial,
        },
        required=("category", "traversal"),
        timeout=timeout,
    )


def list_security_news_events(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    timeline: str | None = None,
    window: Mapping[str, Any] | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListSecurityNewsEvents``；请求 ``SecurityNewsEventsRequest``，返回 ``SecurityNewsItemsResult``。"""

    return _call_typed(
        "list_security_news_events",
        params,
        {
            "security": security,
            "timeline": timeline,
            "window": window,
        },
        required=("security", "timeline", "window"),
        timeout=timeout,
    )


def list_security_news_markers(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    timeline: str | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListSecurityNewsMarkers``；请求 ``SecurityNewsMarkersRequest``，返回 ``SecurityNewsItemsResult``。"""

    return _call_typed(
        "list_security_news_markers",
        params,
        {
            "security": security,
            "timeline": timeline,
        },
        required=("security", "timeline"),
        timeout=timeout,
    )


def list_security_research_reports(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    traversal: Mapping[str, Any] | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListSecurityResearchReports``；请求 ``SecurityResearchReportsRequest``，返回 ``SecurityResearchReportsResult``。"""

    return _call_typed(
        "list_security_research_reports",
        params,
        {
            "security": security,
            "traversal": traversal,
        },
        required=("security", "traversal"),
        timeout=timeout,
    )


__all__ = [
    "analyze_security_limit_up",
    "get_security_price_limit_events",
    "get_security_short_term_highlights",
    "list_commodity_stock_linkage_news",
    "list_hot_block_calendar_events",
    "list_hot_event_news",
    "list_market_call_auction_unusual_events",
    "list_market_change_events",
    "list_market_short_term_events",
    "list_news_flash_items",
    "list_news_items",
    "list_security_news_events",
    "list_security_news_markers",
    "list_security_research_reports",
]


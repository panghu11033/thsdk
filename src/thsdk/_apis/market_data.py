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


def check_market_timeline_readiness(
    params: ObjectParams | None = None,
    *,
    market: str | None = None,
    time_index_day: str | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``CheckMarketTimelineReadiness``；请求 ``MarketTimelineReadinessRequest``，返回 ``MarketTimelineReadinessResult``。"""

    return _call_typed(
        "check_market_timeline_readiness",
        params,
        {
            "market": market,
            "time_index_day": time_index_day,
        },
        required=("market", "time_index_day"),
        timeout=timeout,
    )


def get_security_trading_timeline(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``GetSecurityTradingTimeline``；请求 ``SecurityTradingTimelineRequest``，返回 ``SecurityTradingTimeline``。"""

    return _call_typed(
        "get_security_trading_timeline",
        params,
        {
            "security": security,
        },
        required=("security",),
        timeout=timeout,
    )


def list_index_call_auction_quotes(
    params: ObjectParams | None = None,
    *,
    index: Mapping[str, Any] | None = None,
    phase: str | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListIndexCallAuctionQuotes``；请求 ``IndexCallAuctionQuotesRequest``，返回 ``list[IndexCallAuctionQuote]``。"""

    return _call_typed(
        "list_index_call_auction_quotes",
        params,
        {
            "index": index,
            "phase": phase,
        },
        required=("index", "phase"),
        timeout=timeout,
    )


def list_security_call_auction_quotes(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    phase: str | None = None,
    date: str | date | datetime | None = None,
    window: Mapping[str, Any] | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListSecurityCallAuctionQuotes``；请求 ``SecurityCallAuctionQuotesRequest``，返回 ``list[CallAuctionQuote]``。"""

    return _call_typed(
        "list_security_call_auction_quotes",
        params,
        {
            "security": security,
            "phase": phase,
            "date": date,
            "window": window,
        },
        required=("security", "phase"),
        datetime_fields=("date",),
        timeout=timeout,
    )


def list_security_corporate_actions(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    start: int | None = None,
    end: int | None = None,
    adjust: int | None = None,
    period: int | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListSecurityCorporateActions``；请求 ``SecurityCorporateActionsRequest``，返回 ``list[CorporateAction]``。"""

    return _call_typed(
        "list_security_corporate_actions",
        params,
        {
            "security": security,
            "start": start,
            "end": end,
            "adjust": adjust,
            "period": period,
        },
        required=("security", "start", "end", "adjust", "period"),
        timeout=timeout,
    )


def list_security_daily_capital_flows(
    params: ObjectParams | None = None,
    *,
    securities: Sequence[SecurityInput] | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListSecurityDailyCapitalFlows``；请求 ``SecurityDailyCapitalFlowsRequest``，返回 ``list[DailyCapitalFlow]``。"""

    return _call_typed(
        "list_security_daily_capital_flows",
        params,
        {
            "securities": securities,
        },
        required=("securities",),
        timeout=timeout,
    )


def list_security_daily_k_lines_with_previous_close(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    start: int | None = None,
    end: int | None = None,
    adjust: int | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListSecurityDailyKLinesWithPreviousClose``；请求 ``DailyKLineRequest``，返回 ``list[DailyKLineWithPreviousClose]``。"""

    return _call_typed(
        "list_security_daily_k_lines_with_previous_close",
        params,
        {
            "security": security,
            "start": start,
            "end": end,
            "adjust": adjust,
        },
        required=("security", "start", "end", "adjust"),
        timeout=timeout,
    )


def list_security_extended_hours_intraday_bars(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    session: str | None = None,
    date: str | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListSecurityExtendedHoursIntradayBars``；请求 ``SecurityExtendedHoursIntradayBarsRequest``，返回 ``list[IntradayBar]``。"""

    return _call_typed(
        "list_security_extended_hours_intraday_bars",
        params,
        {
            "security": security,
            "session": session,
            "date": date,
        },
        required=("security", "session", "date"),
        timeout=timeout,
    )


def list_security_extended_hours_ticks(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    session: str | None = None,
    window: Mapping[str, Any] | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListSecurityExtendedHoursTicks``；请求 ``SecurityExtendedHoursTicksRequest``，返回 ``list[Tick]``。"""

    return _call_typed(
        "list_security_extended_hours_ticks",
        params,
        {
            "security": security,
            "session": session,
            "window": window,
        },
        required=("security", "session", "window"),
        timeout=timeout,
    )


def list_security_financial_snapshots(
    params: ObjectParams | None = None,
    *,
    securities: Sequence[SecurityInput] | None = None,
    fields: Sequence[str] | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListSecurityFinancialSnapshots``；请求 ``SecurityFinancialSnapshotsRequest``，返回 ``list[SecurityFinancialSnapshot]``。"""

    return _call_typed(
        "list_security_financial_snapshots",
        params,
        {
            "securities": securities,
            "fields": fields,
        },
        required=("securities", "fields"),
        timeout=timeout,
    )


def list_security_intraday_bars(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    date: str | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListSecurityIntradayBars``；请求 ``IntradayBarsRequest``，返回 ``list[IntradayBar]``。"""

    return _call_typed(
        "list_security_intraday_bars",
        params,
        {
            "security": security,
            "date": date,
        },
        required=("security", "date"),
        timeout=timeout,
    )


def list_security_k_lines(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    start: int | None = None,
    end: int | None = None,
    adjust: int | None = None,
    period: int | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListSecurityKLines``；请求 ``KLineRequest``，返回 ``list[KLine]``。"""

    return _call_typed(
        "list_security_k_lines",
        params,
        {
            "security": security,
            "start": start,
            "end": end,
            "adjust": adjust,
            "period": period,
        },
        required=("security", "start", "end", "adjust", "period"),
        timeout=timeout,
    )


def list_security_option_greeks(
    params: ObjectParams | None = None,
    *,
    securities: Sequence[SecurityInput] | None = None,
    metrics: Sequence[int] | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListSecurityOptionGreeks``；请求 ``OptionGreeksRequest``，返回 ``list[OptionGreeksRow]``。"""

    return _call_typed(
        "list_security_option_greeks",
        params,
        {
            "securities": securities,
            "metrics": metrics,
        },
        required=("securities",),
        timeout=timeout,
    )


def list_security_order_books(
    params: ObjectParams | None = None,
    *,
    securities: Sequence[SecurityInput] | None = None,
    depth: str | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListSecurityOrderBooks``；请求 ``SecurityOrderBooksRequest``，返回 ``list[SecurityOrderBook]``。"""

    return _call_typed(
        "list_security_order_books",
        params,
        {
            "securities": securities,
            "depth": depth,
        },
        required=("securities", "depth"),
        timeout=timeout,
    )


def list_security_price_volume_levels(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListSecurityPriceVolumeLevels``；请求 ``SecurityPriceVolumeLevelsRequest``，返回 ``list[PriceVolumeLevel]``。"""

    return _call_typed(
        "list_security_price_volume_levels",
        params,
        {
            "security": security,
        },
        required=("security",),
        timeout=timeout,
    )


def list_security_ticks(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    window: Mapping[str, Any] | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListSecurityTicks``；请求 ``SecurityTicksRequest``，返回 ``list[Tick]``。"""

    return _call_typed(
        "list_security_ticks",
        params,
        {
            "security": security,
            "window": window,
        },
        required=("security", "window"),
        timeout=timeout,
    )


def list_security_time_and_sales_ticks(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    count: int | None = None,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListSecurityTimeAndSalesTicks``；请求 ``SecurityTimeAndSalesTicksRequest``，返回 ``list[Tick]``。"""

    return _call_typed(
        "list_security_time_and_sales_ticks",
        params,
        {
            "security": security,
            "count": count,
        },
        required=("security", "count"),
        timeout=timeout,
    )


__all__ = [
    "check_market_timeline_readiness",
    "get_security_trading_timeline",
    "list_index_call_auction_quotes",
    "list_security_call_auction_quotes",
    "list_security_corporate_actions",
    "list_security_daily_capital_flows",
    "list_security_daily_k_lines_with_previous_close",
    "list_security_extended_hours_intraday_bars",
    "list_security_extended_hours_ticks",
    "list_security_financial_snapshots",
    "list_security_intraday_bars",
    "list_security_k_lines",
    "list_security_option_greeks",
    "list_security_order_books",
    "list_security_price_volume_levels",
    "list_security_ticks",
    "list_security_time_and_sales_ticks",
]


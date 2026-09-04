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


def calculate_security_realtime_statistics(
    params: ObjectParams | None = None,
    *,
    securities: Sequence[SecurityInput] | None = None,
    metrics: Sequence[int] | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``CalculateSecurityRealtimeStatistics``；请求 ``RealtimeStatsCalculationRequest``，返回 ``RealtimeStatsResult``。"""

    return _call_typed(
        "calculate_security_realtime_statistics",
        params,
        {
            "securities": securities,
            "metrics": metrics,
        },
        required=("securities", "metrics"),
        timeout=timeout,
        extra=extra,
    )


def get_security_popularity_rank(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    benchmark: Mapping[str, Any] | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``GetSecurityPopularityRank``；请求 ``PopularityRankRequest``，返回 ``PopularityRankResult``。"""

    return _call_typed(
        "get_security_popularity_rank",
        params,
        {
            "security": security,
            "benchmark": benchmark,
        },
        required=("security",),
        timeout=timeout,
        extra=extra,
    )


def list_securities_by_realtime_signal(
    params: ObjectParams | None = None,
    *,
    markets: Sequence[str] | None = None,
    signal: str | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``ListSecuritiesByRealtimeSignal``；请求 ``RealtimeSignalSecuritiesRequest``，返回 ``list[RealtimeSignalSecurity]``。"""

    return _call_typed(
        "list_securities_by_realtime_signal",
        params,
        {
            "markets": markets,
            "signal": signal,
        },
        required=("markets", "signal"),
        timeout=timeout,
        extra=extra,
    )


def rank_block_securities(
    params: ObjectParams | None = None,
    *,
    block: BlockInput | None = None,
    sort_begin: int | None = None,
    sort_count: int | None = None,
    sort_id: str | None = None,
    sort_order: str | None = None,
    exclude_securities: Sequence[SecurityInput] | None = None,
    exclude_blocks: Sequence[BlockInput] | None = None,
    func_period: str | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``RankBlockSecurities``；请求 ``SortedBlockSecuritiesRequest``，返回 ``SortedSecuritiesResult``。"""

    return _call_typed(
        "rank_block_securities",
        params,
        {
            "block": block,
            "sort_begin": sort_begin,
            "sort_count": sort_count,
            "sort_id": sort_id,
            "sort_order": sort_order,
            "exclude_securities": exclude_securities,
            "exclude_blocks": exclude_blocks,
            "func_period": func_period,
        },
        required=("block",),
        timeout=timeout,
        extra=extra,
    )


def rank_block_securities_by_industry(
    params: ObjectParams | None = None,
    *,
    block: BlockInput | None = None,
    sort_begin: int | None = None,
    sort_count: int | None = None,
    sort_order: str | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``RankBlockSecuritiesByIndustry``；请求 ``IndustrySortedBlockSecuritiesRequest``，返回 ``SortedSecuritiesResult``。"""

    return _call_typed(
        "rank_block_securities_by_industry",
        params,
        {
            "block": block,
            "sort_begin": sort_begin,
            "sort_count": sort_count,
            "sort_order": sort_order,
        },
        required=("block",),
        timeout=timeout,
        extra=extra,
    )


def rank_constituents_by_performance_contribution(
    params: ObjectParams | None = None,
    *,
    code: str | None = None,
    market: str | None = None,
    target: str | None = None,
    sort_id: int | None = None,
    sort_order: str | None = None,
    sort_begin: int | None = None,
    sort_count: int | None = None,
    valid_begin: int | None = None,
    valid_end: int | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``RankConstituentsByPerformanceContribution``；请求 ``PerformanceContributionRankingRequest``，返回 ``list[PerformanceContributionItem]``。"""

    return _call_typed(
        "rank_constituents_by_performance_contribution",
        params,
        {
            "code": code,
            "market": market,
            "target": target,
            "sort_id": sort_id,
            "sort_order": sort_order,
            "sort_begin": sort_begin,
            "sort_count": sort_count,
            "valid_begin": valid_begin,
            "valid_end": valid_end,
        },
        required=("code", "market"),
        timeout=timeout,
        extra=extra,
    )


def rank_related_securities(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    sort_begin: int | None = None,
    sort_count: int | None = None,
    sort_id: str | None = None,
    sort_order: str | None = None,
    func_period: str | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``RankRelatedSecurities``；请求 ``RelatedSecuritiesRequest``，返回 ``SortedSecuritiesResult``。"""

    return _call_typed(
        "rank_related_securities",
        params,
        {
            "security": security,
            "sort_begin": sort_begin,
            "sort_count": sort_count,
            "sort_id": sort_id,
            "sort_order": sort_order,
            "func_period": func_period,
        },
        required=("security",),
        timeout=timeout,
        extra=extra,
    )


def rank_securities_by_popularity(
    params: ObjectParams | None = None,
    *,
    type: int | None = None,
    benchmark: Mapping[str, Any] | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``RankSecuritiesByPopularity``；请求 ``PopularityRankTopRequest``，返回 ``PopularityRankTopResult``。"""

    return _call_typed(
        "rank_securities_by_popularity",
        params,
        {
            "type": type,
            "benchmark": benchmark,
        },
        required=(),
        timeout=timeout,
        extra=extra,
    )


def rank_securities_by_realtime_statistic(
    params: ObjectParams | None = None,
    *,
    markets: Sequence[str] | None = None,
    securities: Sequence[SecurityInput] | None = None,
    sort_by: int | None = None,
    sort_dir: str | None = None,
    sort_begin: int | None = None,
    sort_count: int | None = None,
    exclude_securities: Sequence[SecurityInput] | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``RankSecuritiesByRealtimeStatistic``；请求 ``RealtimeStatsRankingRequest``，返回 ``RealtimeStatsResult``。"""

    return _call_typed(
        "rank_securities_by_realtime_statistic",
        params,
        {
            "markets": markets,
            "securities": securities,
            "sort_by": sort_by,
            "sort_dir": sort_dir,
            "sort_begin": sort_begin,
            "sort_count": sort_count,
            "exclude_securities": exclude_securities,
        },
        required=("sort_by",),
        timeout=timeout,
        extra=extra,
    )


def sort_securities(
    params: ObjectParams | None = None,
    *,
    securities: Sequence[SecurityInput] | None = None,
    sort_begin: int | None = None,
    sort_count: int | None = None,
    sort_id: str | None = None,
    sort_order: str | None = None,
    func_period: str | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``SortSecurities``；请求 ``SortedSecuritiesRequest``，返回 ``SortedSecuritiesResult``。"""

    return _call_typed(
        "sort_securities",
        params,
        {
            "securities": securities,
            "sort_begin": sort_begin,
            "sort_count": sort_count,
            "sort_id": sort_id,
            "sort_order": sort_order,
            "func_period": func_period,
        },
        required=("securities",),
        timeout=timeout,
        extra=extra,
    )


def sort_securities_by_industry(
    params: ObjectParams | None = None,
    *,
    securities: Sequence[SecurityInput] | None = None,
    sort_begin: int | None = None,
    sort_count: int | None = None,
    sort_order: str | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``SortSecuritiesByIndustry``；请求 ``IndustrySortedSecuritiesRequest``，返回 ``SortedSecuritiesResult``。"""

    return _call_typed(
        "sort_securities_by_industry",
        params,
        {
            "securities": securities,
            "sort_begin": sort_begin,
            "sort_count": sort_count,
            "sort_order": sort_order,
        },
        required=("securities",),
        timeout=timeout,
        extra=extra,
    )


__all__ = [
    "calculate_security_realtime_statistics",
    "get_security_popularity_rank",
    "list_securities_by_realtime_signal",
    "rank_block_securities",
    "rank_block_securities_by_industry",
    "rank_constituents_by_performance_contribution",
    "rank_related_securities",
    "rank_securities_by_popularity",
    "rank_securities_by_realtime_statistic",
    "sort_securities",
    "sort_securities_by_industry",
]


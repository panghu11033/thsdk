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


def list_wencai_expression_fields(query: str, *, timeout: float | None = None) -> Any:
    """调用原生 ``ListWencaiExpressionFields``，返回 ``list[WencaiField]``。"""

    return _call_string("list_wencai_expression_fields", query, argument="query", timeout=timeout)


def list_wencai_hot_blocks(
    params: ObjectParams | None = None,
    *,
    kind: str | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``ListWencaiHotBlocks``；请求 ``WencaiHotBlocksRequest``，返回 ``WencaiHotBlocksResult``。"""

    return _call_typed(
        "list_wencai_hot_blocks",
        params,
        {
            "kind": kind,
        },
        required=("kind",),
        timeout=timeout,
        extra=extra,
    )


def query_wencai(
    params: ObjectParams | None = None,
    *,
    query: str | None = None,
    markets: Sequence[str] | None = None,
    limit: int | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``QueryWencai``；请求 ``WencaiQueryRequest``，返回 ``WencaiQueryResult``。"""

    return _call_typed(
        "query_wencai",
        params,
        {
            "query": query,
            "markets": markets,
            "limit": limit,
        },
        required=("query",),
        timeout=timeout,
        extra=extra,
    )


def query_wencai_realtime_fields(
    params: ObjectParams | None = None,
    *,
    securities: Sequence[SecurityInput] | None = None,
    fields: Sequence[Mapping[str, Any]] | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``QueryWencaiRealtimeFields``；请求 ``WencaiRealtimeFieldsRequest``，返回 ``WencaiRealtimeFieldsResult``。"""

    return _call_typed(
        "query_wencai_realtime_fields",
        params,
        {
            "securities": securities,
            "fields": fields,
        },
        required=("securities", "fields"),
        timeout=timeout,
        extra=extra,
    )


def query_wencai_securities(
    params: ObjectParams | None = None,
    *,
    query: str | None = None,
    markets: Sequence[str] | None = None,
    limit: int | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``QueryWencaiSecurities``；请求 ``WencaiSecuritiesRequest``，返回 ``WencaiSecuritiesResult``。"""

    return _call_typed(
        "query_wencai_securities",
        params,
        {
            "query": query,
            "markets": markets,
            "limit": limit,
        },
        required=("query",),
        timeout=timeout,
        extra=extra,
    )


def rank_block_securities_by_wencai_field(
    params: ObjectParams | None = None,
    *,
    block: BlockInput | None = None,
    field: Mapping[str, Any] | None = None,
    offset: int | None = None,
    limit: int | None = None,
    sort_order: str | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``RankBlockSecuritiesByWencaiField``；请求 ``RankBlockSecuritiesByWencaiFieldRequest``，返回 ``WencaiBlockRankingResult``。"""

    return _call_typed(
        "rank_block_securities_by_wencai_field",
        params,
        {
            "block": block,
            "field": field,
            "offset": offset,
            "limit": limit,
            "sort_order": sort_order,
        },
        required=("block", "field"),
        timeout=timeout,
        extra=extra,
    )


def resolve_wencai_securities(
    params: ObjectParams | None = None,
    *,
    query: str | None = None,
    limit: int | None = None,
    stock_suffix: str | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``ResolveWencaiSecurities``；请求 ``ResolveWencaiSecuritiesRequest``，返回 ``ResolvedWencaiSecuritiesResult``。"""

    return _call_typed(
        "resolve_wencai_securities",
        params,
        {
            "query": query,
            "limit": limit,
            "stock_suffix": stock_suffix,
        },
        required=("query",),
        timeout=timeout,
        extra=extra,
    )


__all__ = [
    "list_wencai_expression_fields",
    "list_wencai_hot_blocks",
    "query_wencai",
    "query_wencai_realtime_fields",
    "query_wencai_securities",
    "rank_block_securities_by_wencai_field",
    "resolve_wencai_securities",
]


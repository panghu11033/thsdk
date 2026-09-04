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


def get_market_metadata(
    params: ObjectParams | None = None,
    *,
    market: str | None = None,
    version_flag: int | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``GetMarketMetadata``；请求 ``MarketMetadataRequest``，返回 ``MarketMetadata``。"""

    return _call_typed(
        "get_market_metadata",
        params,
        {
            "market": market,
            "version_flag": version_flag,
        },
        required=("market",),
        timeout=timeout,
        extra=extra,
    )


def get_market_security_names(
    params: ObjectParams | None = None,
    *,
    market: str | None = None,
    realtime_version_ini: str | None = None,
    history_version_ini: str | None = None,
    base_version_ini: str | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``GetMarketSecurityNames``；请求 ``MarketSecurityNamesRequest``，返回 ``MarketSecurityNamesResult``。"""

    return _call_typed(
        "get_market_security_names",
        params,
        {
            "market": market,
            "realtime_version_ini": realtime_version_ini,
            "history_version_ini": history_version_ini,
            "base_version_ini": base_version_ini,
        },
        required=("market",),
        timeout=timeout,
        extra=extra,
    )


def get_security_concept_tags(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``GetSecurityConceptTags``；请求 ``SecurityConceptTagsRequest``，返回 ``SecurityConceptTagsResult``。"""

    return _call_typed(
        "get_security_concept_tags",
        params,
        {
            "security": security,
        },
        required=("security",),
        timeout=timeout,
        extra=extra,
    )


def get_security_industry(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``GetSecurityIndustry``；请求 ``SecurityRequest``，返回 ``SecurityIndustryMapping``。"""

    return _call_typed(
        "get_security_industry",
        params,
        {
            "security": security,
        },
        required=("security",),
        timeout=timeout,
        extra=extra,
    )


def list_block_constituents(
    params: ObjectParams | None = None,
    *,
    block: BlockInput | None = None,
    sort_begin: int | None = None,
    sort_count: int | None = None,
    sort_order: str | None = None,
    sort_id: str | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``ListBlockConstituents``；请求 ``BlockConstituentsRequest``，返回 ``list[BlockConstituent]``。"""

    return _call_typed(
        "list_block_constituents",
        params,
        {
            "block": block,
            "sort_begin": sort_begin,
            "sort_count": sort_count,
            "sort_order": sort_order,
            "sort_id": sort_id,
        },
        required=("block",),
        timeout=timeout,
        extra=extra,
    )


def list_block_descriptions(
    params: ObjectParams | None = None,
    *,
    blocks: Sequence[BlockInput] | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``ListBlockDescriptions``；请求 ``BlockDescriptionsRequest``，返回 ``list[BlockDescription]``。"""

    return _call_typed(
        "list_block_descriptions",
        params,
        {
            "blocks": blocks,
        },
        required=("blocks",),
        timeout=timeout,
        extra=extra,
    )


def list_futures_related_securities(*, timeout: float | None = None) -> Any:
    """调用原生 ``ListFuturesRelatedSecurities``，返回 ``list[FuturesRelatedSecurity]``。"""

    return _call_none("list_futures_related_securities", timeout=timeout)


def list_industry_children(
    params: ObjectParams | None = None,
    *,
    industry: Mapping[str, Any] | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``ListIndustryChildren``；请求 ``IndustryChildrenRequest``，返回 ``list[IndustryChild]``。"""

    return _call_typed(
        "list_industry_children",
        params,
        {
            "industry": industry,
        },
        required=("industry",),
        timeout=timeout,
        extra=extra,
    )


def list_market_securities(
    params: ObjectParams | None = None,
    *,
    market: str | None = None,
    sort_begin: int | None = None,
    sort_count: int | None = None,
    sort_id: str | None = None,
    sort_order: str | None = None,
    func_period: str | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``ListMarketSecurities``；请求 ``MarketSecuritiesRequest``，返回 ``MarketSecuritiesResult``。"""

    return _call_typed(
        "list_market_securities",
        params,
        {
            "market": market,
            "sort_begin": sort_begin,
            "sort_count": sort_count,
            "sort_id": sort_id,
            "sort_order": sort_order,
            "func_period": func_period,
        },
        required=("market",),
        timeout=timeout,
        extra=extra,
    )


def list_related_security_performances(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``ListRelatedSecurityPerformances``；请求 ``RelatedSecurityPerformancesRequest``，返回 ``list[RelatedSecurityPerformance]``。"""

    return _call_typed(
        "list_related_security_performances",
        params,
        {
            "security": security,
        },
        required=("security",),
        timeout=timeout,
        extra=extra,
    )


def list_security_ah_relations(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``ListSecurityAHRelations``；请求 ``SecurityAHRelationsRequest``，返回 ``list[SecurityAHRelation]``。"""

    return _call_typed(
        "list_security_ah_relations",
        params,
        {
            "security": security,
        },
        required=("security",),
        timeout=timeout,
        extra=extra,
    )


def list_security_block_memberships(
    params: ObjectParams | None = None,
    *,
    security: SecurityInput | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``ListSecurityBlockMemberships``；请求 ``SecurityBlockMembershipsRequest``，返回 ``list[SecurityBlockMembership]``。"""

    return _call_typed(
        "list_security_block_memberships",
        params,
        {
            "security": security,
        },
        required=("security",),
        timeout=timeout,
        extra=extra,
    )


def list_security_futures_relations(
    securities: Sequence[SecurityInput],
    *,
    timeout: float | None = None,
) -> Any:
    """调用原生 ``ListSecurityFuturesRelations``，返回 ``list[SecurityFuturesRelation]``。"""

    return _call_securities("list_security_futures_relations", securities, timeout=timeout)


def list_security_industry_mappings(
    params: ObjectParams | None = None,
    *,
    securities: Sequence[SecurityInput] | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``ListSecurityIndustryMappings``；请求 ``SecurityIndustryMappingsRequest``，返回 ``list[SecurityIndustryMapping]``。"""

    return _call_typed(
        "list_security_industry_mappings",
        params,
        {
            "securities": securities,
        },
        required=("securities",),
        timeout=timeout,
        extra=extra,
    )


def list_security_link_relations(link_key: str, *, timeout: float | None = None) -> Any:
    """调用原生 ``ListSecurityLinkRelations``，返回 ``list[SecurityLinkRelation]``。"""

    return _call_string("list_security_link_relations", link_key, argument="link_key", timeout=timeout)


def resolve_block(
    params: ObjectParams | None = None,
    *,
    name: str | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``ResolveBlock``；请求 ``ResolveBlockRequest``，返回 ``Block``。"""

    return _call_typed(
        "resolve_block",
        params,
        {
            "name": name,
        },
        required=("name",),
        timeout=timeout,
        extra=extra,
    )


def resolve_securities(
    params: ObjectParams | None = None,
    *,
    codes: Sequence[str] | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``ResolveSecurities``；请求 ``ResolveSecuritiesRequest``，返回 ``list[ResolvedSecurity]``。"""

    return _call_typed(
        "resolve_securities",
        params,
        {
            "codes": codes,
        },
        required=("codes",),
        timeout=timeout,
        extra=extra,
    )


def search_securities(
    params: ObjectParams | None = None,
    *,
    pattern: str | None = None,
    market: str | None = None,
    timeout: float | None = None,
    **extra: Any,
) -> Any:
    """调用原生 ``SearchSecurities``；请求 ``SearchSecuritiesRequest``，返回 ``list[SecurityCandidate]``。"""

    return _call_typed(
        "search_securities",
        params,
        {
            "pattern": pattern,
            "market": market,
        },
        required=("pattern",),
        timeout=timeout,
        extra=extra,
    )


__all__ = [
    "get_market_metadata",
    "get_market_security_names",
    "get_security_concept_tags",
    "get_security_industry",
    "list_block_constituents",
    "list_block_descriptions",
    "list_futures_related_securities",
    "list_industry_children",
    "list_market_securities",
    "list_related_security_performances",
    "list_security_ah_relations",
    "list_security_block_memberships",
    "list_security_futures_relations",
    "list_security_industry_mappings",
    "list_security_link_relations",
    "resolve_block",
    "resolve_securities",
    "search_securities",
]


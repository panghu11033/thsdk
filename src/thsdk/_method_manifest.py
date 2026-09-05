from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Literal


RequestKind = Literal["none", "object", "string", "securities"]


@dataclass(frozen=True, slots=True)
class NativeMethodSpec:
    """描述一个可调用 Canonical 方法的稳定元数据。"""

    name: str
    go_name: str
    category: str
    request_kind: RequestKind
    request_type: str | None
    result_type: str
    mutating: bool = False
    request_fields: tuple[str, ...] = ()
    required_fields: tuple[str, ...] = ()
    returns_dataframe: bool = False
    dataframe_rows_field: str | None = None


_REQUEST_CONTRACTS = MappingProxyType(
    {
        "account_permissions": ((), ()),
        "add_account_watchlist_group_securities": (
            ("group_id", "securities"),
            ("group_id", "securities"),
        ),
        "add_account_watchlist_securities": (
            ("securities", "add_to_front"),
            ("securities",),
        ),
        "analyze_security_limit_up": (("security", "date"), ("security",)),
        "calculate_security_realtime_statistics": (
            ("securities", "metrics"),
            ("securities", "metrics"),
        ),
        "check_market_timeline_readiness": (
            ("market", "time_index_day"),
            ("market", "time_index_day"),
        ),
        "clear_account_watchlist": ((), ()),
        "create_account_watchlist_group": (
            ("name", "securities"),
            ("name",),
        ),
        "delete_account_watchlist_group": (("group_id",), ("group_id",)),
        "get_account_watchlist": ((), ()),
        "get_account_watchlist_groups": ((), ()),
        "get_market_metadata": (("market", "version_flag"), ("market",)),
        "get_market_security_names": (
            (
                "market",
                "realtime_version_ini",
                "history_version_ini",
                "base_version_ini",
            ),
            ("market",),
        ),
        "get_security_concept_tags": (("security",), ("security",)),
        "get_security_industry": (("security",), ("security",)),
        "get_security_popularity_rank": (
            ("security", "benchmark"),
            ("security",),
        ),
        "get_security_price_limit_events": (
            ("security", "start_year", "end_year"),
            ("security",),
        ),
        "get_security_short_term_highlights": (("security",), ("security",)),
        "get_security_trading_timeline": (("security",), ("security",)),
        "list_block_constituents": (
            ("block", "sort_begin", "sort_count", "sort_order", "sort_id"),
            ("block",),
        ),
        "list_block_descriptions": (("blocks",), ("blocks",)),
        "list_commodity_stock_linkage_news": (
            ("commodity_index",),
            ("commodity_index",),
        ),
        "list_futures_related_securities": ((), ()),
        "list_hot_block_calendar_events": ((), ()),
        "list_hot_event_news": (("block", "range"), ("block",)),
        "list_index_call_auction_quotes": (
            ("index", "phase"),
            ("index", "phase"),
        ),
        "list_industry_children": (("industry",), ("industry",)),
        "list_market_call_auction_unusual_events": (
            ("market", "trade_date"),
            ("market",),
        ),
        "list_market_change_events": ((), ()),
        "list_market_securities": (
            (
                "market",
                "sort_begin",
                "sort_count",
                "sort_id",
                "sort_order",
                "func_period",
            ),
            ("market",),
        ),
        "list_market_short_term_events": (
            (
                "market",
                "mode",
                "securities",
                "max_count",
                "before_timestamp_micros",
            ),
            ("market", "mode"),
        ),
        "list_news_flash_items": (
            (
                "traversal",
                "tag",
                "tag_id",
                "page",
                "page_size",
                "page_time",
                "sequence",
                "created_at",
                "environment",
            ),
            ("traversal",),
        ),
        "list_news_items": (
            (
                "category",
                "security",
                "market",
                "traversal",
                "summary_mode",
                "advertorial",
            ),
            ("category", "traversal"),
        ),
        "list_related_security_performances": (("security",), ("security",)),
        "list_securities_by_realtime_signal": (
            ("markets", "signal"),
            ("markets", "signal"),
        ),
        "list_security_ah_relations": (("security",), ("security",)),
        "list_security_block_memberships": (("security",), ("security",)),
        "list_security_call_auction_quotes": (
            ("security", "phase", "date", "window"),
            ("security", "phase"),
        ),
        "list_security_corporate_actions": (
            ("security", "start", "end", "adjust", "period"),
            ("security", "start", "end", "adjust", "period"),
        ),
        "list_security_daily_capital_flows": (
            ("securities",),
            ("securities",),
        ),
        "list_security_daily_k_lines_with_previous_close": (
            ("security", "start", "end", "adjust"),
            ("security", "start", "end", "adjust"),
        ),
        "list_security_extended_hours_intraday_bars": (
            ("security", "session", "date"),
            ("security", "session", "date"),
        ),
        "list_security_extended_hours_ticks": (
            ("security", "session", "window"),
            ("security", "session", "window"),
        ),
        "list_security_financial_snapshots": (
            ("securities", "fields"),
            ("securities", "fields"),
        ),
        "list_security_futures_relations": (
            ("securities",),
            ("securities",),
        ),
        "list_security_industry_mappings": (
            ("securities",),
            ("securities",),
        ),
        "list_security_intraday_bars": (
            ("security", "date"),
            ("security", "date"),
        ),
        "list_security_k_lines": (
            ("security", "start", "end", "adjust", "period"),
            ("security", "start", "end", "adjust", "period"),
        ),
        "list_security_link_relations": (("link_key",), ("link_key",)),
        "list_security_news_events": (
            ("security", "timeline", "window"),
            ("security", "timeline", "window"),
        ),
        "list_security_news_markers": (
            ("security", "timeline"),
            ("security", "timeline"),
        ),
        "list_security_option_greeks": (
            ("securities", "metrics"),
            ("securities",),
        ),
        "list_security_order_books": (
            ("securities", "depth"),
            ("securities", "depth"),
        ),
        "list_security_price_volume_levels": (("security",), ("security",)),
        "list_security_research_reports": (
            ("security", "traversal"),
            ("security", "traversal"),
        ),
        "list_security_ticks": (
            ("security", "window"),
            ("security", "window"),
        ),
        "list_security_time_and_sales_ticks": (
            ("security", "count"),
            ("security", "count"),
        ),
        "list_wencai_expression_fields": (("query",), ("query",)),
        "list_wencai_hot_blocks": (("kind",), ("kind",)),
        "query_wencai": (("query", "markets", "limit"), ("query",)),
        "query_wencai_realtime_fields": (
            ("securities", "fields"),
            ("securities", "fields"),
        ),
        "query_wencai_securities": (
            ("query", "markets", "limit"),
            ("query",),
        ),
        "rank_block_securities": (
            (
                "block",
                "sort_begin",
                "sort_count",
                "sort_id",
                "sort_order",
                "exclude_securities",
                "exclude_blocks",
                "func_period",
            ),
            ("block",),
        ),
        "rank_block_securities_by_industry": (
            ("block", "sort_begin", "sort_count", "sort_order"),
            ("block",),
        ),
        "rank_block_securities_by_wencai_field": (
            ("block", "field", "offset", "limit", "sort_order"),
            ("block", "field"),
        ),
        "rank_constituents_by_performance_contribution": (
            (
                "code",
                "market",
                "target",
                "sort_id",
                "sort_order",
                "sort_begin",
                "sort_count",
                "valid_begin",
                "valid_end",
            ),
            ("code", "market"),
        ),
        "rank_related_securities": (
            (
                "security",
                "sort_begin",
                "sort_count",
                "sort_id",
                "sort_order",
                "func_period",
            ),
            ("security",),
        ),
        "rank_securities_by_popularity": (("type", "benchmark"), ()),
        "rank_securities_by_realtime_statistic": (
            (
                "markets",
                "securities",
                "sort_by",
                "sort_dir",
                "sort_begin",
                "sort_count",
                "exclude_securities",
            ),
            ("sort_by",),
        ),
        "remove_account_watchlist_group_securities": (
            ("group_id", "securities"),
            ("group_id", "securities"),
        ),
        "remove_account_watchlist_securities": (
            ("securities",),
            ("securities",),
        ),
        "rename_account_watchlist_group": (
            ("group_id", "name"),
            ("group_id", "name"),
        ),
        "replace_account_watchlist_group_securities": (
            ("group_id", "securities"),
            ("group_id", "securities"),
        ),
        "replace_account_watchlist_securities": (
            ("version", "securities"),
            ("version", "securities"),
        ),
        "resolve_block": (("name",), ("name",)),
        "resolve_securities": (("codes",), ("codes",)),
        "resolve_wencai_securities": (
            ("query", "limit", "stock_suffix"),
            ("query",),
        ),
        "search_securities": (("pattern", "market"), ("pattern",)),
        "sort_securities": (
            (
                "securities",
                "sort_begin",
                "sort_count",
                "sort_id",
                "sort_order",
                "func_period",
            ),
            ("securities",),
        ),
        "sort_securities_by_industry": (
            ("securities", "sort_begin", "sort_count", "sort_order"),
            ("securities",),
        ),
    }
)


# 包装结果类型中的主记录集合。原生直接返回 list[T] 的方法不需要在这里重复声明；
# 它们由 result_type 稳定识别。这里逐项列出 envelope/map 类型，避免根据运行时
# 某次响应中“第一个 list 字段”猜测主表，尤其是问财、涨跌停和快讯这类同时包含
# 多个列表字段的结果。
_DATAFRAME_ROWS_BY_RESULT_TYPE = MappingProxyType(
    {
        "AccountWatchlistGroups": "groups",
        "AccountWatchlistSnapshot": "securities",
        "CommodityStockLinkageNewsResult": "items",
        "HotBlockCalendarResult": "items",
        "HotEventNewsResult": "items",
        "MarketMetadata": "sections",
        "MarketSecuritiesResult": "securities",
        "MarketSecurityNamesResult": "items",
        "NewsFlashItemsResult": "items",
        "NewsItemsResult": "items",
        "PopularityRankTopResult": "items",
        "PriceLimitEventsResult": "events",
        "RealtimeStatsResult": "rows",
        "ResolvedWencaiSecuritiesResult": "items",
        "SecurityConceptTagsResult": "tags",
        "SecurityNewsItemsResult": "items",
        "SecurityResearchReportsResult": "items",
        "SecurityTradingTimeline": "items",
        "SortedSecuritiesResult": "securities",
        "WencaiBlockRankingResult": "items",
        "WencaiHotBlocksResult": "items",
        "WencaiQueryResult": "rows",
        "WencaiRealtimeFieldsResult": "rows",
        "WencaiSecuritiesResult": "items",
    }
)


def _spec(
    name: str,
    go_name: str,
    category: str,
    request_kind: RequestKind,
    request_type: str | None,
    result_type: str,
    *,
    mutating: bool = False,
) -> NativeMethodSpec:
    request_fields, required_fields = _REQUEST_CONTRACTS[name]
    dataframe_rows_field = _DATAFRAME_ROWS_BY_RESULT_TYPE.get(result_type)
    return NativeMethodSpec(
        name=name,
        go_name=go_name,
        category=category,
        request_kind=request_kind,
        request_type=request_type,
        result_type=result_type,
        request_fields=request_fields,
        required_fields=required_fields,
        mutating=mutating,
        returns_dataframe=(
            not mutating
            and (
                result_type.startswith("list[")
                or dataframe_rows_field is not None
            )
        ),
        dataframe_rows_field=None if mutating else dataframe_rows_field,
    )


_SPECS = (
    _spec("account_permissions", "AccountPermissions", "account", "none", None, "AccountPermissions"),
    _spec("add_account_watchlist_group_securities", "AddAccountWatchlistGroupSecurities", "account", "object", "AccountWatchlistGroupSecuritiesRequest", "AccountWatchlistGroups", mutating=True),
    _spec("add_account_watchlist_securities", "AddAccountWatchlistSecurities", "account", "object", "AddAccountWatchlistSecuritiesRequest", "AccountWatchlistUpdate", mutating=True),
    _spec("analyze_security_limit_up", "AnalyzeSecurityLimitUp", "news", "object", "SecurityLimitUpAnalysisRequest", "SecurityLimitUpAnalysisResult"),
    _spec("calculate_security_realtime_statistics", "CalculateSecurityRealtimeStatistics", "rankings", "object", "RealtimeStatsCalculationRequest", "RealtimeStatsResult"),
    _spec("check_market_timeline_readiness", "CheckMarketTimelineReadiness", "market_data", "object", "MarketTimelineReadinessRequest", "MarketTimelineReadinessResult"),
    _spec("clear_account_watchlist", "ClearAccountWatchlist", "account", "none", None, "AccountWatchlistUpdate", mutating=True),
    _spec("create_account_watchlist_group", "CreateAccountWatchlistGroup", "account", "object", "CreateAccountWatchlistGroupRequest", "AccountWatchlistGroups", mutating=True),
    _spec("delete_account_watchlist_group", "DeleteAccountWatchlistGroup", "account", "object", "DeleteAccountWatchlistGroupRequest", "AccountWatchlistGroups", mutating=True),
    _spec("get_account_watchlist", "GetAccountWatchlist", "account", "none", None, "AccountWatchlistSnapshot"),
    _spec("get_account_watchlist_groups", "GetAccountWatchlistGroups", "account", "none", None, "AccountWatchlistGroups"),
    _spec("get_market_metadata", "GetMarketMetadata", "securities", "object", "MarketMetadataRequest", "MarketMetadata"),
    _spec("get_market_security_names", "GetMarketSecurityNames", "securities", "object", "MarketSecurityNamesRequest", "MarketSecurityNamesResult"),
    _spec("get_security_concept_tags", "GetSecurityConceptTags", "securities", "object", "SecurityConceptTagsRequest", "SecurityConceptTagsResult"),
    _spec("get_security_industry", "GetSecurityIndustry", "securities", "object", "SecurityRequest", "SecurityIndustryMapping"),
    _spec("get_security_popularity_rank", "GetSecurityPopularityRank", "rankings", "object", "PopularityRankRequest", "PopularityRankResult"),
    _spec("get_security_price_limit_events", "GetSecurityPriceLimitEvents", "news", "object", "PriceLimitEventsRequest", "PriceLimitEventsResult"),
    _spec("get_security_short_term_highlights", "GetSecurityShortTermHighlights", "news", "object", "SecurityShortTermHighlightsRequest", "SecurityShortTermHighlightsResult"),
    _spec("get_security_trading_timeline", "GetSecurityTradingTimeline", "market_data", "object", "SecurityTradingTimelineRequest", "SecurityTradingTimeline"),
    _spec("list_block_constituents", "ListBlockConstituents", "securities", "object", "BlockConstituentsRequest", "list[BlockConstituent]"),
    _spec("list_block_descriptions", "ListBlockDescriptions", "securities", "object", "BlockDescriptionsRequest", "list[BlockDescription]"),
    _spec("list_commodity_stock_linkage_news", "ListCommodityStockLinkageNews", "news", "object", "CommodityStockLinkageNewsRequest", "CommodityStockLinkageNewsResult"),
    _spec("list_futures_related_securities", "ListFuturesRelatedSecurities", "securities", "none", None, "list[FuturesRelatedSecurity]"),
    _spec("list_hot_block_calendar_events", "ListHotBlockCalendarEvents", "news", "none", None, "HotBlockCalendarResult"),
    _spec("list_hot_event_news", "ListHotEventNews", "news", "object", "HotEventNewsRequest", "HotEventNewsResult"),
    _spec("list_index_call_auction_quotes", "ListIndexCallAuctionQuotes", "market_data", "object", "IndexCallAuctionQuotesRequest", "list[IndexCallAuctionQuote]"),
    _spec("list_industry_children", "ListIndustryChildren", "securities", "object", "IndustryChildrenRequest", "list[IndustryChild]"),
    _spec("list_market_call_auction_unusual_events", "ListMarketCallAuctionUnusualEvents", "news", "object", "CallAuctionUnusualEventsRequest", "list[ShortTermEvent]"),
    _spec("list_market_change_events", "ListMarketChangeEvents", "news", "none", None, "list[MarketChangeEvent]"),
    _spec("list_market_securities", "ListMarketSecurities", "securities", "object", "MarketSecuritiesRequest", "MarketSecuritiesResult"),
    _spec("list_market_short_term_events", "ListMarketShortTermEvents", "news", "object", "MarketShortTermEventsRequest", "list[ShortTermEvent]"),
    _spec("list_news_flash_items", "ListNewsFlashItems", "news", "object", "NewsFlashItemsRequest", "NewsFlashItemsResult"),
    _spec("list_news_items", "ListNewsItems", "news", "object", "NewsItemsRequest", "NewsItemsResult"),
    _spec("list_related_security_performances", "ListRelatedSecurityPerformances", "securities", "object", "RelatedSecurityPerformancesRequest", "list[RelatedSecurityPerformance]"),
    _spec("list_securities_by_realtime_signal", "ListSecuritiesByRealtimeSignal", "rankings", "object", "RealtimeSignalSecuritiesRequest", "list[RealtimeSignalSecurity]"),
    _spec("list_security_ah_relations", "ListSecurityAHRelations", "securities", "object", "SecurityAHRelationsRequest", "list[SecurityAHRelation]"),
    _spec("list_security_block_memberships", "ListSecurityBlockMemberships", "securities", "object", "SecurityBlockMembershipsRequest", "list[SecurityBlockMembership]"),
    _spec("list_security_call_auction_quotes", "ListSecurityCallAuctionQuotes", "market_data", "object", "SecurityCallAuctionQuotesRequest", "list[CallAuctionQuote]"),
    _spec("list_security_corporate_actions", "ListSecurityCorporateActions", "market_data", "object", "SecurityCorporateActionsRequest", "list[CorporateAction]"),
    _spec("list_security_daily_capital_flows", "ListSecurityDailyCapitalFlows", "market_data", "object", "SecurityDailyCapitalFlowsRequest", "list[DailyCapitalFlow]"),
    _spec("list_security_daily_k_lines_with_previous_close", "ListSecurityDailyKLinesWithPreviousClose", "market_data", "object", "DailyKLineRequest", "list[DailyKLineWithPreviousClose]"),
    _spec("list_security_extended_hours_intraday_bars", "ListSecurityExtendedHoursIntradayBars", "market_data", "object", "SecurityExtendedHoursIntradayBarsRequest", "list[IntradayBar]"),
    _spec("list_security_extended_hours_ticks", "ListSecurityExtendedHoursTicks", "market_data", "object", "SecurityExtendedHoursTicksRequest", "list[Tick]"),
    _spec("list_security_financial_snapshots", "ListSecurityFinancialSnapshots", "market_data", "object", "SecurityFinancialSnapshotsRequest", "list[SecurityFinancialSnapshot]"),
    _spec("list_security_futures_relations", "ListSecurityFuturesRelations", "securities", "securities", "list[Security]", "list[SecurityFuturesRelation]"),
    _spec("list_security_industry_mappings", "ListSecurityIndustryMappings", "securities", "object", "SecurityIndustryMappingsRequest", "list[SecurityIndustryMapping]"),
    _spec("list_security_intraday_bars", "ListSecurityIntradayBars", "market_data", "object", "IntradayBarsRequest", "list[IntradayBar]"),
    _spec("list_security_k_lines", "ListSecurityKLines", "market_data", "object", "KLineRequest", "list[KLine]"),
    _spec("list_security_link_relations", "ListSecurityLinkRelations", "securities", "string", "linkKey string", "list[SecurityLinkRelation]"),
    _spec("list_security_news_events", "ListSecurityNewsEvents", "news", "object", "SecurityNewsEventsRequest", "SecurityNewsItemsResult"),
    _spec("list_security_news_markers", "ListSecurityNewsMarkers", "news", "object", "SecurityNewsMarkersRequest", "SecurityNewsItemsResult"),
    _spec("list_security_option_greeks", "ListSecurityOptionGreeks", "market_data", "object", "OptionGreeksRequest", "list[OptionGreeksRow]"),
    _spec("list_security_order_books", "ListSecurityOrderBooks", "market_data", "object", "SecurityOrderBooksRequest", "list[SecurityOrderBook]"),
    _spec("list_security_price_volume_levels", "ListSecurityPriceVolumeLevels", "market_data", "object", "SecurityPriceVolumeLevelsRequest", "list[PriceVolumeLevel]"),
    _spec("list_security_research_reports", "ListSecurityResearchReports", "news", "object", "SecurityResearchReportsRequest", "SecurityResearchReportsResult"),
    _spec("list_security_ticks", "ListSecurityTicks", "market_data", "object", "SecurityTicksRequest", "list[Tick]"),
    _spec("list_security_time_and_sales_ticks", "ListSecurityTimeAndSalesTicks", "market_data", "object", "SecurityTimeAndSalesTicksRequest", "list[Tick]"),
    _spec("list_wencai_expression_fields", "ListWencaiExpressionFields", "wencai", "string", "query string", "list[WencaiField]"),
    _spec("list_wencai_hot_blocks", "ListWencaiHotBlocks", "wencai", "object", "WencaiHotBlocksRequest", "WencaiHotBlocksResult"),
    _spec("query_wencai", "QueryWencai", "wencai", "object", "WencaiQueryRequest", "WencaiQueryResult"),
    _spec("query_wencai_realtime_fields", "QueryWencaiRealtimeFields", "wencai", "object", "WencaiRealtimeFieldsRequest", "WencaiRealtimeFieldsResult"),
    _spec("query_wencai_securities", "QueryWencaiSecurities", "wencai", "object", "WencaiSecuritiesRequest", "WencaiSecuritiesResult"),
    _spec("rank_block_securities", "RankBlockSecurities", "rankings", "object", "SortedBlockSecuritiesRequest", "SortedSecuritiesResult"),
    _spec("rank_block_securities_by_industry", "RankBlockSecuritiesByIndustry", "rankings", "object", "IndustrySortedBlockSecuritiesRequest", "SortedSecuritiesResult"),
    _spec("rank_block_securities_by_wencai_field", "RankBlockSecuritiesByWencaiField", "wencai", "object", "RankBlockSecuritiesByWencaiFieldRequest", "WencaiBlockRankingResult"),
    _spec("rank_constituents_by_performance_contribution", "RankConstituentsByPerformanceContribution", "rankings", "object", "PerformanceContributionRankingRequest", "list[PerformanceContributionItem]"),
    _spec("rank_related_securities", "RankRelatedSecurities", "rankings", "object", "RelatedSecuritiesRequest", "SortedSecuritiesResult"),
    _spec("rank_securities_by_popularity", "RankSecuritiesByPopularity", "rankings", "object", "PopularityRankTopRequest", "PopularityRankTopResult"),
    _spec("rank_securities_by_realtime_statistic", "RankSecuritiesByRealtimeStatistic", "rankings", "object", "RealtimeStatsRankingRequest", "RealtimeStatsResult"),
    _spec("remove_account_watchlist_group_securities", "RemoveAccountWatchlistGroupSecurities", "account", "object", "AccountWatchlistGroupSecuritiesRequest", "AccountWatchlistGroups", mutating=True),
    _spec("remove_account_watchlist_securities", "RemoveAccountWatchlistSecurities", "account", "object", "RemoveAccountWatchlistSecuritiesRequest", "AccountWatchlistUpdate", mutating=True),
    _spec("rename_account_watchlist_group", "RenameAccountWatchlistGroup", "account", "object", "RenameAccountWatchlistGroupRequest", "AccountWatchlistGroups", mutating=True),
    _spec("replace_account_watchlist_group_securities", "ReplaceAccountWatchlistGroupSecurities", "account", "object", "AccountWatchlistGroupSecuritiesRequest", "AccountWatchlistGroups", mutating=True),
    _spec("replace_account_watchlist_securities", "ReplaceAccountWatchlistSecurities", "account", "object", "ReplaceAccountWatchlistSecuritiesRequest", "AccountWatchlistUpdate", mutating=True),
    _spec("resolve_block", "ResolveBlock", "securities", "object", "ResolveBlockRequest", "Block"),
    _spec("resolve_securities", "ResolveSecurities", "securities", "object", "ResolveSecuritiesRequest", "list[ResolvedSecurity]"),
    _spec("resolve_wencai_securities", "ResolveWencaiSecurities", "wencai", "object", "ResolveWencaiSecuritiesRequest", "ResolvedWencaiSecuritiesResult"),
    _spec("search_securities", "SearchSecurities", "securities", "object", "SearchSecuritiesRequest", "list[SecurityCandidate]"),
    _spec("sort_securities", "SortSecurities", "rankings", "object", "SortedSecuritiesRequest", "SortedSecuritiesResult"),
    _spec("sort_securities_by_industry", "SortSecuritiesByIndustry", "rankings", "object", "IndustrySortedSecuritiesRequest", "SortedSecuritiesResult"),
)


NATIVE_METHOD_SPECS = _SPECS
NATIVE_METHODS = MappingProxyType({spec.name: spec for spec in _SPECS})
NATIVE_METHOD_NAMES = tuple(spec.name for spec in _SPECS)
MUTATING_METHOD_NAMES = frozenset(spec.name for spec in _SPECS if spec.mutating)
DATAFRAME_METHOD_NAMES = frozenset(
    spec.name for spec in _SPECS if spec.returns_dataframe
)


def method_inventory() -> tuple[NativeMethodSpec, ...]:
    """返回完整的 80 项同步 Canonical API 清单。"""

    return NATIVE_METHOD_SPECS


if len(NATIVE_METHODS) != 80:
    raise RuntimeError("THSDK native method manifest must contain exactly 80 unique methods")
if set(_REQUEST_CONTRACTS) != set(NATIVE_METHODS):
    raise RuntimeError("THSDK request contracts must match the native method manifest")
if any(
    len(spec.request_fields) != len(set(spec.request_fields))
    or not set(spec.required_fields).issubset(spec.request_fields)
    for spec in _SPECS
):
    raise RuntimeError("THSDK request fields must be unique and contain every required field")
if any(
    (spec.request_kind == "none") != (not spec.request_fields)
    or spec.request_kind in {"string", "securities"}
    and spec.request_fields != spec.required_fields
    for spec in _SPECS
):
    raise RuntimeError("THSDK request fields do not match their request kinds")
if any(
    spec.name.startswith("list_") and not spec.returns_dataframe
    or spec.mutating and spec.returns_dataframe
    or spec.dataframe_rows_field is not None and not spec.returns_dataframe
    for spec in _SPECS
):
    raise RuntimeError("THSDK DataFrame contracts do not match method semantics")
if len(DATAFRAME_METHOD_NAMES) != 63 or DATAFRAME_METHOD_NAMES & MUTATING_METHOD_NAMES:
    raise RuntimeError("THSDK must expose exactly 63 read-only DataFrame methods")
_FORBIDDEN_METHOD_MARKERS = ("subscribe", "subscription", "level2", "query_data")
if any(
    marker in f"{spec.name} {spec.go_name}".lower()
    for spec in _SPECS
    for marker in _FORBIDDEN_METHOD_MARKERS
):
    raise RuntimeError(
        "subscription, Level-2, and query_data methods must not enter the THSDK manifest"
    )


__all__ = [
    "DATAFRAME_METHOD_NAMES",
    "NativeMethodSpec",
    "method_inventory",
]

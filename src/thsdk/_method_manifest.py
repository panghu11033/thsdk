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
    return NativeMethodSpec(
        name=name,
        go_name=go_name,
        category=category,
        request_kind=request_kind,
        request_type=request_type,
        result_type=result_type,
        mutating=mutating,
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


def method_inventory() -> tuple[NativeMethodSpec, ...]:
    """返回完整的 80 项同步 Canonical API 清单。"""

    return NATIVE_METHOD_SPECS


if len(NATIVE_METHODS) != 80:
    raise RuntimeError("THSDK native method manifest must contain exactly 80 unique methods")
if any(name.startswith("subscribe") or "level2" in name for name in NATIVE_METHODS):
    raise RuntimeError("subscription and Level-2 methods must not enter the THSDK manifest")


__all__ = ["NativeMethodSpec", "method_inventory"]

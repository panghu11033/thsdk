from __future__ import annotations

from enum import Enum, IntEnum


class Adjust(IntEnum):
    NONE = 0
    FORWARD = 1
    BACKWARD = 2


class Period(IntEnum):
    MINUTE_1 = 0x3001
    MINUTE_5 = 0x3005
    MINUTE_15 = 0x300F
    MINUTE_30 = 0x301E
    MINUTE_60 = 0x303C
    MINUTE_120 = 0x3078
    DAY = 0x4000
    WEEK = 0x5001
    MONTH = 0x6001
    QUARTER = 0x6003
    YEAR = 0x7001


class CallAuctionPhase(str, Enum):
    OPENING = "opening"
    CLOSING = "closing"
    CUSTOM = "custom"


class IndexCallAuctionPhase(str, Enum):
    OPENING = "opening"
    CLOSING = "closing"


class ExtendedHoursSession(str, Enum):
    PRE_MARKET = "pre_market"
    POST_MARKET = "post_market"


class OrderBookDepth(str, Enum):
    FIVE = "5"


class NewsFlashTraversalMode(str, Enum):
    PAGE = "page"
    OLDER = "older"
    NEWER = "newer"


class NewsTimeline(str, Enum):
    HISTORICAL = "historical"
    REALTIME = "realtime"


class NewsTraversalMode(str, Enum):
    PAGE = "page"
    SINCE = "since"


class NewsDirection(str, Enum):
    FIRST = "first"
    OLDER = "older"
    NEWER = "newer"


class InfoType(IntEnum):
    BAD = -1
    HISTORY_TIME = 2053
    REALTIME = 2054
    NEWS_REPORT = 8193
    SH_SZ_FUND = 10240
    FOREIGN_EXCHANGE_NEWS = 10241
    FOREIGN_EXCHANGE_FX = 10242
    FOREIGN_EXCHANGE_CJ = 10243
    GLOBAL_MARKET = 10244
    GLOBAL_FINANCE = 10245
    GLOBAL_ECONOMIC_DATA = 10246
    STOCK_INFO = 14339
    INDUSTRY_INFO = 14340
    ANNOUNCEMENT = 14341
    STOCK_RESEARCH_REPORT = 14342
    INDUSTRY_RESEARCH_REPORT = 14343
    SECURITY_TAPE_READING = 14348
    INDEX_FUTURES = 14349
    MARKET_TAPE_READING = 14355
    MARKET_NEWS = 14356
    MARKET_TREND_READING = 14359
    GLT_MESSAGE = 14363
    NEW_STOCK_INFO = 14364
    MULTIPLY_FUTURES = 14365
    NEEQ_NEWS = 14366
    NEEQ_SECONDARY_NEWS = 14367
    COMMODITY_INDEX = 14368
    SECURITY_INSIGHT = 14371
    SH_TO_HK_NEWS = 32769
    HK_NEWS = 32770
    USA_NEWS = 32770
    HK_PAN_INFO = 32771


class InfoSummaryMode(IntEnum):
    DEFAULT = 0
    DISABLED = 1
    ENABLED = 2


class RealtimeStatsMetric(IntEnum):
    FIRST_LIMIT_UP_TIME = 330323
    FINAL_LIMIT_UP_TIME = 330324
    LIMIT_UP_TYPE = 330325
    LIMIT_UP_STATE = 330329


class RealtimeSecuritySignal(str, Enum):
    LIMIT_UP = "limit_up"
    LIMIT_DOWN = "limit_down"
    LIMIT_UP_BREAK = "limit_up_break"
    LIMIT_DOWN_BREAK = "limit_down_break"


class FinancialSnapshotField(str, Enum):
    TOTAL_SHARES = "total_shares"
    FLOAT_SHARES = "float_shares"
    NET_ASSET_PER_SHARE = "net_asset_per_share"


class OptionGreeksMetric(IntEnum):
    IMPLIED_VOLATILITY = 920341
    HISTORY_VOLATILITY = 723853
    REAL_LEVER_RATIO = 2980
    THEORY_PRICE = 920342
    DELTA = 723854
    GAMMA = 723855
    RHO = 723856
    THETA = 723857
    VEGA = 723858


class WencaiHotBlockKind(str, Enum):
    CONCEPT = "concept"
    INDUSTRY = "industry"


class HotEventNewsRange(str, Enum):
    RECENT = "recent"
    HISTORICAL = "historical"


class ShortTermEventMode(str, Enum):
    MARKET_RECENT = "market_recent"
    SECURITY_SCOPED = "security_scoped"


class PerformanceContributionTarget(str, Enum):
    INDEX = "index"
    SECURITY = "security"


class PopularityRankTopType(IntEnum):
    ALL_STOCKS = 1


__all__ = [
    "Adjust",
    "Period",
    "CallAuctionPhase",
    "IndexCallAuctionPhase",
    "ExtendedHoursSession",
    "OrderBookDepth",
    "NewsFlashTraversalMode",
    "NewsTimeline",
    "NewsTraversalMode",
    "NewsDirection",
    "InfoType",
    "InfoSummaryMode",
    "RealtimeStatsMetric",
    "RealtimeSecuritySignal",
    "FinancialSnapshotField",
    "OptionGreeksMetric",
    "WencaiHotBlockKind",
    "HotEventNewsRange",
    "ShortTermEventMode",
    "PerformanceContributionTarget",
    "PopularityRankTopType",
]

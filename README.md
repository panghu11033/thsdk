# THSDK

## 介绍

THSDK 是面向 Python 的同步证券数据 SDK，覆盖实时与历史行情、证券与板块资料、资讯事件、
问财选股、排行统计以及账号自选管理。安装后直接调用 `thsdk` 模块，无需创建客户端对象。

常用查询和多数多行接口返回 `pandas.DataFrame`，方便继续筛选、分析或导出。当前版本只提供
同步查询与账号自选管理，不包含订阅、Level-2 或任意原始方法分发入口。

## 安装

```bash
pip install --upgrade thsdk
```


## 认证

调用数据接口前，从下面三种登录方式中任选一种：

| 登录方式 | 调用 | 说明 |
| --- | --- | --- |
| 自动登录 | `thsdk.auth()` | 复用当前进程或本地会话；没有可用会话时使用临时账号 |
| 账号密码 | `thsdk.auth("username", "password")` | 使用传入的账号和密码登录 |
| 扫码登录 | `thsdk.auth_qrcode()` | 优先复用本地会话，否则显示二维码并等待扫码 |

```python
import thsdk

# 三选一
thsdk.auth()
# thsdk.auth("username", "password")
# thsdk.auth_qrcode()
```

登录成功后，可复用会话保存在首次调用时工作目录的 `account.session`。请把它视为敏感凭据，
不要提交到 Git 或交给他人。`thsdk.logout()` 会退出当前账号并删除该会话文件。临时账号仅适合
体验和只读查询，其数据权限与调用频率可能受限。

## 使用案例

以下案例均先完成导入与认证：

```python
import thsdk

thsdk.auth()
```

### 行情查询

```python
daily = thsdk.get_price(
    "USHA600519",
    frequency="daily",
    count=20,
    fq="pre",
)
intraday = thsdk.intraday_data("USHA600519")
order_book = thsdk.depth(["USHA600519", "USZA300033"])

print(daily)
print(intraday)
print(order_book)
```

接口使用“4 位市场代码 + 证券代码”的完整标识，例如 `USHA600519`、`USZA300033`。
只有名称或短代码时，可先调用 `search_symbols()` 或 `complete_ths_code()`。

### 问财、板块与资讯

```python
stock_pool = thsdk.wencai_nlp("市盈率小于 20，净利润增长率大于 20%", limit=50)
members = thsdk.block_constituents("沪深300", count=20)
flash_news = thsdk.news(page=1, page_size=20)

print(stock_pool)
print(members)
print(flash_news)
```

### 标准 API

标准 API 与底层运行组件的方法一一对应，可直接传入完整请求字段：

```python
rows = thsdk.list_security_k_lines(
    security="USHA600519",
    start=-20,
    end=0,
    adjust=thsdk.Adjust.FORWARD,
    period=thsdk.Period.DAY,
)
print(rows)
```

数据接口只返回结果，不会主动打印。`thsdk/examples/` 包含 102 个脚本：96 个公开函数的同名
最小示例、5 个组合流程，以及用于观察 50ms 限频的 `loop.py`；账号写操作与 `logout()` 的示例
默认不会执行。

## 全部公开 API

THSDK 3.x 公开 96 个函数。12 个便捷数据 API 建立在标准 API 之上，因此两层能力存在重叠。

| 接口层 | 数量 | 说明 |
| --- | ---: | --- |
| 认证、会话与清单 | 4 | 登录、退出和标准 API 静态清单 |
| 便捷数据 API | 12 | 适配常用参数并返回 `pandas.DataFrame` |
| 标准 API | 80 | 与底层运行组件的同步业务方法一一对应 |

12 个便捷数据 API 和 63 个多行标准 API 返回 `pandas.DataFrame`；7 个单对象读取和
10 个账号写操作保留运行组件解码后的 `dict` 或标量。标准 API 可直接传关键字字段，
也可把完整请求映射作为第一个参数；所有标准 API 都接受可选的 `timeout=`。

### 认证、会话与清单（4）

| API | 用途 |
| --- | --- |
| `auth()` | 自动登录，或使用传入的账号密码登录 |
| `auth_qrcode()` | 恢复本地会话，必要时显示二维码并等待扫码 |
| `logout()` | 退出账号并删除持久会话 |
| `method_inventory()` | 返回 80 个标准 API 的静态元数据 |

### 便捷数据 API（12）

| API | 用途 |
| --- | --- |
| `get_price()` | 查询一只证券的 K 线，可按日期、条数、周期、复权和字段筛选 |
| `klines()` | 使用传统参数名查询 K 线 |
| `intraday_data()` | 查询当天或指定交易日的分时走势 |
| `tick_level1()` | 按最近条数或时间范围查询普通逐笔成交 |
| `depth()` | 查询一只或多只证券的五档买卖盘并按档位展开 |
| `corporate_action()` | 查询分红、送转、配股和除权除息记录 |
| `search_symbols()` | 按代码、拼音或中文名称搜索证券 |
| `complete_ths_code()` | 把一个或多个短代码解析为完整证券代码 |
| `wencai_nlp()` | 执行自然语言选股并把动态字段展开为表格列 |
| `news()` | 分页查询 7x24 快讯 |
| `market_securities()` | 分页列出指定市场中的证券 |
| `block_constituents()` | 按板块 ID 或名称查询成分证券 |

### 账户权限与自选股（13）

| API | 用途 | 类型 |
| --- | --- | --- |
| `account_permissions()` | 查询当前账号的数据权限 | 读 |
| `get_account_watchlist()` | 查询账号自选股及版本信息 | 读 |
| `get_account_watchlist_groups()` | 查询自选分组及分组证券 | 读 |
| `add_account_watchlist_group_securities()` | 向指定自选分组追加证券 | 写 |
| `add_account_watchlist_securities()` | 向账号自选股追加证券 | 写 |
| `clear_account_watchlist()` | 清空账号全部自选股 | 写 |
| `create_account_watchlist_group()` | 创建自选分组，可同时设置初始证券 | 写 |
| `delete_account_watchlist_group()` | 删除指定自选分组 | 写 |
| `remove_account_watchlist_group_securities()` | 从指定自选分组移除证券 | 写 |
| `remove_account_watchlist_securities()` | 从账号自选股移除证券 | 写 |
| `rename_account_watchlist_group()` | 重命名自选分组 | 写 |
| `replace_account_watchlist_group_securities()` | 整体替换指定分组中的证券 | 写 |
| `replace_account_watchlist_securities()` | 按版本整体替换账号自选股 | 写 |

10 个写接口会修改远端账号数据，其中 `clear_account_watchlist()` 会清空全部自选股，请只在明确
需要时调用。

### 市场目录、证券发现与关系（18）

| API | 用途 |
| --- | --- |
| `get_market_metadata()` | 查询市场元数据和版本信息 |
| `get_market_security_names()` | 查询指定市场的证券名称数据 |
| `get_security_concept_tags()` | 查询证券所属概念标签 |
| `get_security_industry()` | 查询证券的行业归属 |
| `list_block_constituents()` | 查询板块成分证券并支持服务端排序 |
| `list_block_descriptions()` | 批量查询板块名称和简介 |
| `list_futures_related_securities()` | 查询期货相关证券目录 |
| `list_industry_children()` | 查询行业节点的下级行业 |
| `list_market_securities()` | 分页查询指定市场的证券 |
| `list_related_security_performances()` | 查询关联证券及其表现 |
| `list_security_ah_relations()` | 查询证券的 A/H 股对应关系 |
| `list_security_block_memberships()` | 查询证券所属板块 |
| `list_security_futures_relations()` | 批量查询证券与期货的关联关系 |
| `list_security_industry_mappings()` | 批量查询证券的行业映射 |
| `list_security_link_relations()` | 按关联键查询证券链接关系 |
| `resolve_block()` | 按名称或条件解析唯一板块标识 |
| `resolve_securities()` | 批量解析短代码或候选证券 |
| `search_securities()` | 按代码、拼音或名称搜索证券候选项 |

### 行情、交易序列与基本面（17）

| API | 用途 |
| --- | --- |
| `check_market_timeline_readiness()` | 检查市场交易时间线数据是否就绪 |
| `get_security_trading_timeline()` | 查询证券交易时段和时间线 |
| `list_index_call_auction_quotes()` | 查询指数集合竞价行情 |
| `list_security_call_auction_quotes()` | 查询证券集合竞价行情 |
| `list_security_corporate_actions()` | 查询公司行为和除权除息资料 |
| `list_security_daily_capital_flows()` | 查询证券每日资金流 |
| `list_security_daily_k_lines_with_previous_close()` | 查询带前收盘价的日 K 线 |
| `list_security_extended_hours_intraday_bars()` | 查询盘前盘后分时数据 |
| `list_security_extended_hours_ticks()` | 查询盘前盘后逐笔数据 |
| `list_security_financial_snapshots()` | 批量查询证券财务快照字段 |
| `list_security_intraday_bars()` | 查询指定交易日分时数据 |
| `list_security_k_lines()` | 查询多周期、可复权的历史 K 线 |
| `list_security_option_greeks()` | 查询期权 Greeks 指标 |
| `list_security_order_books()` | 批量查询证券盘口 |
| `list_security_price_volume_levels()` | 查询价量分布档位 |
| `list_security_ticks()` | 查询证券逐笔成交 |
| `list_security_time_and_sales_ticks()` | 查询成交明细时间序列 |

### 资讯、事件与异动（14）

| API | 用途 |
| --- | --- |
| `analyze_security_limit_up()` | 分析证券涨停状态与相关信息 |
| `get_security_price_limit_events()` | 查询证券涨跌停事件 |
| `get_security_short_term_highlights()` | 查询证券短线亮点 |
| `list_commodity_stock_linkage_news()` | 查询商品与股票联动资讯 |
| `list_hot_block_calendar_events()` | 查询热门板块日历事件 |
| `list_hot_event_news()` | 查询热点事件资讯 |
| `list_market_call_auction_unusual_events()` | 查询市场集合竞价异动 |
| `list_market_change_events()` | 查询市场异动事件 |
| `list_market_short_term_events()` | 查询市场短线事件 |
| `list_news_flash_items()` | 分页查询 7x24 快讯 |
| `list_news_items()` | 按分类、证券或市场查询资讯 |
| `list_security_news_events()` | 按时间线查询证券资讯事件 |
| `list_security_news_markers()` | 查询证券资讯时间标记 |
| `list_security_research_reports()` | 查询证券研究报告 |

### 问财（7）

| API | 用途 |
| --- | --- |
| `list_wencai_expression_fields()` | 解析问财表达式可用字段 |
| `list_wencai_hot_blocks()` | 查询问财热门板块 |
| `query_wencai()` | 执行问财查询并返回字段和行数据 |
| `query_wencai_realtime_fields()` | 查询证券的问财实时字段 |
| `query_wencai_securities()` | 执行问财选股并返回证券结果 |
| `rank_block_securities_by_wencai_field()` | 按问财字段对板块成分排序 |
| `resolve_wencai_securities()` | 把问财条件解析为标准证券池 |

### 实时统计、排行与排序（11）

| API | 用途 |
| --- | --- |
| `calculate_security_realtime_statistics()` | 计算一组证券的实时统计指标 |
| `get_security_popularity_rank()` | 查询单只证券的热度排名 |
| `list_securities_by_realtime_signal()` | 按实时信号筛选证券 |
| `rank_block_securities()` | 按指定指标对板块成分排序 |
| `rank_block_securities_by_industry()` | 按行业指标对板块成分排序 |
| `rank_constituents_by_performance_contribution()` | 按涨跌贡献度排行指数或板块成分 |
| `rank_related_securities()` | 对关联证券进行服务端排序 |
| `rank_securities_by_popularity()` | 查询证券热度榜单 |
| `rank_securities_by_realtime_statistic()` | 按实时统计字段排行证券 |
| `sort_securities()` | 按指定指标排序自定义证券池 |
| `sort_securities_by_industry()` | 按行业指标排序自定义证券池 |

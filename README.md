# THSDK

THSDK 是面向 Python 的同步证券数据 SDK。它提供实时与历史行情、证券与板块资料、资讯事件、
问财选股、排行统计以及账号自选管理；安装后直接调用 `thsdk` 模块，无需创建客户端对象。

快速导航：[快速安装](#快速安装) · [快速上手](#快速上手) ·
[连接与认证](#连接与认证4-种用法) · [常用查询](#常用查询与调用约定) ·
[全部 API](#全部公开-api) · [示例](#示例)

## 快速安装

```bash
pip install --upgrade thsdk
```

要求 Python 3.10 或更高版本。发行包内置运行组件，并根据当前系统与处理器自动选择：

| 操作系统 | 架构 |
| --- | --- |
| macOS | Apple Silicon、Intel |
| Linux | arm64、amd64 |
| Windows | amd64 |

## 快速上手

下面是一段可以直接运行的完整代码。首次使用自己的账号时，终端会显示二维码；扫码成功后，
`get_price()` 返回最近 20 条前复权日 K 线：

```python
import thsdk

thsdk.auth_qrcode()

result = thsdk.get_price(
    "USHA600519",
    frequency="daily",
    count=20,
    fq="pre",
)
print(result)
```

认证成功后会保存可复用会话。以后从同一个工作目录运行时，通常只需调用 `auth()`：

```python
import thsdk

thsdk.auth()
result = thsdk.depth(["USHA600519", "USZA300033"])
print(result)
```

数据 API 只返回结果，不会主动打印。普通脚本里如果只写 `thsdk.get_price(...)`，运行成功也可能
看不到输出；需要像上面一样接住返回值并显式 `print()`。

## 主要能力

| 能力 | 内容 |
| --- | --- |
| 行情与基本面 | K 线、分时、逐笔成交、五档盘口、价量分布、资金流、期权 Greeks、财务快照 |
| 证券与板块 | 市场证券、代码搜索与补全、行业、概念、板块成分、A/H 与期货关联 |
| 资讯与事件 | 7x24 快讯、个股资讯、研报、异动、涨跌停、集合竞价与热点日历 |
| 问财 | 自然语言查询、证券池解析、动态字段、实时字段和热门板块 |
| 排行与统计 | 证券和板块排序、热度排行、实时信号、实时指标和贡献度排行 |
| 账号数据 | 权限、自选股、自选分组的查询与显式修改 |

公开函数分为四组：

| 接口组 | 数量 | 说明 |
| --- | ---: | --- |
| 认证与会话 | 3 | `auth()`、`auth_qrcode()`、`logout()` |
| 静态清单 | 1 | `method_inventory()` |
| 便捷数据 API | 12 | 适配常用参数并返回 `pandas.DataFrame` |
| Canonical API | 80 | 与运行组件的同步业务能力一一对应，保留原始请求和返回结构 |

12 个便捷 API 建立在 Canonical API 之上，两层能力存在重叠。当前公开范围不包含订阅、
Level-2 或任意原始方法分发入口。

## 连接与认证：4 种用法

THSDK 由模块内部维护一个进程级客户端。没有公开的 `connect()` 或 `disconnect()`；调用数据 API
前，必须先显式完成下面四种认证用法之一。

| 方式 | 写法 | 适合场景 | 交互行为 |
| --- | --- | --- | --- |
| 1. 扫码认证 | `auth_qrcode()` | 首次绑定自己的账号 | 有有效会话时直接恢复，否则显示二维码并等待扫码 |
| 2. 显式凭据 | `auth(username, password, mac=None)` | 凭据由当前程序安全注入 | 直接使用本次传入的账号重新认证 |
| 3. 环境变量 | 设置 `THS_USERNAME`、`THS_PASSWORD` 后调用 `auth()` | 终端、CI 或密钥管理系统 | 无需把账号密码写进代码 |
| 4. 自动认证 | 无参数调用 `auth()`，且不设置上述环境变量 | 日常复用或临时体验 | 依次复用进程状态、本地会话，最后尝试临时账号 |

### 1. 扫码认证

```python
import thsdk

thsdk.auth_qrcode(timeout=120, poll_interval=1)
```

`auth_qrcode()` 会先尝试恢复当前目录的会话。只有会话不存在或不可用时，才会显示二维码和一个
扫码地址；认证完成后返回 `True`。

### 2. 显式账号密码

```python
import thsdk

thsdk.auth("your_username", "your_password")
```

`mac` 是可选参数；不传时 SDK 会根据账号生成稳定的本地设备标识。账号与密码必须同时提供。

### 3. 环境变量

```bash
export THS_USERNAME=your_username
export THS_PASSWORD=your_password
```

```python
import thsdk

thsdk.auth()
```

两个环境变量必须同时设置且不能为空。

### 4. 自动恢复或临时账号

```python
import thsdk

thsdk.auth()
```

当没有显式凭据和环境变量时，`auth()` 按以下顺序处理：

1. 当前进程已经认证：直接返回。
2. 默认客户端记录的会话目录存在有效 `account.session`：恢复该会话。
3. 没有可用会话：获取临时账号并认证。

临时账号只适合体验和只读查询，其数据权限与调用频率可能受限。

### Session 保存与退出

默认客户端在首次认证或数据调用时记录当时的工作目录，并把持久会话放在该目录的
`account.session`，不会写入 Python 安装目录。进程运行期间再切换工作目录，不会改变这个客户端的
会话位置。

| 操作 | `account.session` |
| --- | --- |
| 正常结束 Python 进程 | 保留，供下次复用 |
| 再次调用 `auth()` 或 `auth_qrcode()` | 尝试复用有效会话 |
| 调用 `logout()` | 退出账号并删除会话 |

请把 `account.session` 当作敏感凭据：不要提交到 Git、公开、复制给其他用户或放入安装包。

## 常用查询与调用约定

下面的示例均假定已经完成导入和认证：

```python
import thsdk

thsdk.auth()
```

### 证券代码

接口使用 `4 位市场代码 + 证券代码` 的完整标识：

| 示例 | 含义 |
| --- | --- |
| `USHA600519` | 沪市 A 股 |
| `USZA300033` | 深市 A 股 |
| `USTM920807` | 北交所证券 |
| `USHI1A0001` | 上证指数 |
| `USZI399006` | 深证指数 |
| `UNQQTSLA` | 美股证券 |
| `URFI881272` | 同花顺行业指数 |
| `URFA884295` | 同花顺三级行业 |

只有名称或短代码时，先搜索或补全：

```python
candidates = thsdk.search_symbols("同花顺", market="USZA")
print(candidates[["full_code", "name"]])

resolved = thsdk.complete_ths_code(["300033", "600519", "159919"])
print(resolved)
```

同一个短代码可能出现在不同市场，不建议只根据数字前缀推断市场。

### 分时、逐笔和盘口

```python
intraday = thsdk.intraday_data("USHA600519")
ticks = thsdk.tick_level1("USHA600519", count=100)
order_book = thsdk.depth(["USHA600519", "USZA300033"])

print(intraday)
print(ticks)
print(order_book)
```

### 问财、快讯和板块

```python
stock_pool = thsdk.wencai_nlp("市盈率小于 20，净利润增长率大于 20%", limit=50)
flash_news = thsdk.news(page=1, page_size=20)
members = thsdk.block_constituents("沪深300", count=20)

print(stock_pool)
print(flash_news)
print(members)
```

### Canonical API 参数

Canonical API 可以直接传关键字字段：

```python
rows = thsdk.list_security_k_lines(
    security="USHA600519",
    start=-20,
    end=0,
    adjust=thsdk.Adjust.FORWARD,
    period=thsdk.Period.DAY,
)
```

也可以把完整请求映射作为第一个参数，但不能再混用请求关键字：

```python
rows = thsdk.list_security_k_lines({
    "security": {"market": "USHA", "code": "600519"},
    "start": -20,
    "end": 0,
    "adjust": 1,
    "period": 0x4000,
})
```

所有 Canonical API 都接受可选的 `timeout=`，它只控制 Python 客户端等待时间。函数签名会列出
可用字段；也可以通过 `help(thsdk.list_security_k_lines)` 查看参数和返回类型。

## 全部公开 API

以下索引覆盖 96 个公开函数，并简要说明每个函数的用途。

### 认证、会话与清单（4）

| API | 用途 |
| --- | --- |
| `auth()` | 使用显式凭据、环境变量、本地会话或临时账号认证 |
| `auth_qrcode()` | 恢复本地会话，必要时显示二维码并等待扫码 |
| `logout()` | 退出账号并删除持久会话；示例默认不执行 |
| `method_inventory()` | 返回 80 个 Canonical API 的静态元数据 |

### 便捷数据 API（12）

这些接口负责常用参数转换，并统一返回 `pandas.DataFrame`。

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

10 个写接口会修改远端账号数据。它们的单 API 示例和写流程默认关闭；特别是
`clear_account_watchlist()`，不要放进批量试跑脚本。

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

## 返回值与错误

便捷数据 API 返回 `pandas.DataFrame`。Canonical API 返回运行组件解码后的 `dict`、`list` 或
标量，不重命名字段、不丢弃未知字段，也不会自动转成 DataFrame。

失败时会抛出异常，不会把失败伪装成空结果：

```python
import thsdk

try:
    thsdk.auth()
    data = thsdk.get_price("USHA600519", count=5)
except thsdk.AuthenticationError as exc:
    print(f"认证失败：{exc}")
except thsdk.APIError as exc:
    print(f"请求失败 [{exc.code}]：{exc}")
```

| 异常 | 含义 |
| --- | --- |
| `THSDKError` | SDK 基础异常 |
| `AuthenticationError` | 凭据、会话或扫码认证失败 |
| `NotAuthenticatedError` | 尚未认证就调用数据 API |
| `APIError` | 运行组件或服务端请求失败，错误码位于 `exc.code` |

## 示例

`thsdk/examples/` 包含 101 个脚本：96 个公开函数各有一个同名最小示例，另有 5 个组合流程。
这些脚本随发行包一同安装，文件名与对应的公开函数一致；常用调用已经整理为本文前面的可复制示例。

账号权限、自选股和自选分组的读取示例不会打印私有返回内容。10 个写接口与 `logout()` 的示例
默认 `EXECUTE = False`，不会认证、删除会话或修改远端账号。

| 流程示例 | 内容 |
| --- | --- |
| `workflow_account_watchlist.py` | 自选股、自选分组和首只自选证券日 K |
| `workflow_account_group_edit.py` | 创建、重命名、增删证券并清理临时分组；默认不执行 |
| `workflow_ths_industry_levels.py` | 个股所属二级行业、三级行业、成分股及涨幅排序 |
| `workflow_concept_block.py` | 热门概念、板块解析、简介和成分股涨幅排序 |
| `workflow_wencai_stock_pool.py` | 问财选股、证券池排序和基本面快照 |

## 常见问题

### 运行脚本没有输出

数据接口不会自动显示返回值。使用 `result = ...` 接住结果，再调用 `print(result)`。

### 扫码函数没有显示新二维码

默认客户端记录的会话目录已有有效 `account.session` 时，`auth_qrcode()` 会直接恢复会话。这是
正常行为；只有会话不可用时才会创建新的扫码任务。

### 如何确认当前有哪些 Canonical API

```python
import thsdk

for spec in thsdk.method_inventory():
    print(spec.category, spec.name, spec.request_type, spec.result_type, spec.mutating)
```

## 许可证

MIT License

import thsdk

thsdk.auth()
result = thsdk.list_news_items(
    category=thsdk.InfoType.STOCK_INFO,
    security="USHA600519",
    traversal={"mode": "since"},
    summary_mode=thsdk.InfoSummaryMode.ENABLED,
    advertorial=False,
)
print(result)

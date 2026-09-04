import thsdk

thsdk.auth()
result = thsdk.list_commodity_stock_linkage_news(
    commodity_index={"id": "S004161736"},
)
print(result)

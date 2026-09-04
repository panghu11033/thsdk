import thsdk

thsdk.auth()
result = thsdk.list_market_securities(
    market="USZA",
    sort_begin=0,
    sort_count=10,
)
print(result)

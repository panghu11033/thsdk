import thsdk

thsdk.auth()
result = thsdk.check_market_timeline_readiness(
    market="SH",
    time_index_day="20260902,20260902,",
)
print(result)

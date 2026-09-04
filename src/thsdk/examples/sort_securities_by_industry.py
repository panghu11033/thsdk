import thsdk

thsdk.auth()
result = thsdk.sort_securities_by_industry(
    securities=["USZA300033", "USHA600519"],
    sort_begin=0,
    sort_count=10,
    sort_order="D",
)
print(result)

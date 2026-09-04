import thsdk

thsdk.auth()
result = thsdk.sort_securities(
    securities=["USZA300033", "USHA600519"],
    sort_begin=0,
    sort_count=10,
    sort_id="55",
    sort_order="D",
)
print(result)

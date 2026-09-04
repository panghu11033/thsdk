import thsdk

thsdk.auth()
result = thsdk.list_securities_by_realtime_signal(
    markets=["USHA", "USZA"],
    signal="limit_up",
)
print(result)

import thsdk

thsdk.auth()
result = thsdk.list_security_intraday_bars(
    security="USHA600519",
    date="0",
)
print(result)

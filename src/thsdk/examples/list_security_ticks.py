import thsdk

thsdk.auth()
result = thsdk.list_security_ticks(
    security="USHA600519",
    window={"count": 10},
)
print(result)

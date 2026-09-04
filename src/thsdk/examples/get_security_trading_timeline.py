import thsdk

thsdk.auth()
result = thsdk.get_security_trading_timeline(security="USHA600519")
print(result)

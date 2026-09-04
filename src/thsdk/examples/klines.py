import thsdk

thsdk.auth()
result = thsdk.klines("USHA600519", count=10)
print(result)

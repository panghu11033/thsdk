import thsdk

thsdk.auth()
result = thsdk.get_price("USHA600519", count=10)
print(result)

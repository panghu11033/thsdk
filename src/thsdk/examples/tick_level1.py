import thsdk

thsdk.auth()
result = thsdk.tick_level1("USHA600519", count=10)
print(result)

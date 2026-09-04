import thsdk

thsdk.auth()
result = thsdk.intraday_data("USHA600519")
print(result)

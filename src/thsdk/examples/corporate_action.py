import thsdk

thsdk.auth()
result = thsdk.corporate_action("USHA600519", count=10)
print(result)

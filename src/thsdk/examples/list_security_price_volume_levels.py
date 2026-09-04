import thsdk

thsdk.auth()
result = thsdk.list_security_price_volume_levels(security="USHA600519")
print(result)

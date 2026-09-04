import thsdk

thsdk.auth()
result = thsdk.list_related_security_performances(security="USZA300033")
print(result)

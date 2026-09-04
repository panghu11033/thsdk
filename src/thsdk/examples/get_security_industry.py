import thsdk

thsdk.auth()
result = thsdk.get_security_industry(security="USZA300033")
print(result)

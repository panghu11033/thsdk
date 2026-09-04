import thsdk

thsdk.auth()
result = thsdk.get_security_popularity_rank(security="USZA300033")
print(result)

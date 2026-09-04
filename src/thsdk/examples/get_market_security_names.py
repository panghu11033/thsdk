import thsdk

thsdk.auth()
result = thsdk.get_market_security_names(market="USZA")
print(result)

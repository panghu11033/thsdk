import thsdk

thsdk.auth()
result = thsdk.get_market_metadata(market="USZA")
print(result)

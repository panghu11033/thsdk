import thsdk

thsdk.auth()
result = thsdk.market_securities("USZA", start=0, count=10)
print(result)

import thsdk

thsdk.auth()
result = thsdk.block_constituents("沪深300", start=0, count=10)
print(result)

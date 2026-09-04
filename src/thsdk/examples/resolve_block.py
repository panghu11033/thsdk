import thsdk

thsdk.auth()
result = thsdk.resolve_block(name="沪深300")
print(result)

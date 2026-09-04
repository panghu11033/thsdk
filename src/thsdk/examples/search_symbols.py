import thsdk

thsdk.auth()
result = thsdk.search_symbols("同花顺", market="USZA")
print(result)

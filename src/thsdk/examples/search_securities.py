import thsdk

thsdk.auth()
result = thsdk.search_securities(pattern="同花顺", market="USZA")
print(result)

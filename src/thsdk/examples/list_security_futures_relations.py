import thsdk

thsdk.auth()
result = thsdk.list_security_futures_relations(["USZA300033"])
print(result)

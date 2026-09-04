import thsdk

thsdk.auth()
result = thsdk.list_security_ah_relations(security="USHA601318")
print(result)

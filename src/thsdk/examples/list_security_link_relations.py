import thsdk

thsdk.auth()
result = thsdk.list_security_link_relations("stock_16_Z_A")
print(result)

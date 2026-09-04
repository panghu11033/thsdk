import thsdk

thsdk.auth()
result = thsdk.list_security_block_memberships(security="USZA300033")
print(result)

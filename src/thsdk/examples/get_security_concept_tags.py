import thsdk

thsdk.auth()
result = thsdk.get_security_concept_tags(security="USZA300033")
print(result)

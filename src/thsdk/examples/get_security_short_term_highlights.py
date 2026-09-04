import thsdk

thsdk.auth()
result = thsdk.get_security_short_term_highlights(security="USHA600519")
print(result)

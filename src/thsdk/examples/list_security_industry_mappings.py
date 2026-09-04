import thsdk

thsdk.auth()
result = thsdk.list_security_industry_mappings(
    securities=["USZA300033", "USHA600519"],
)
print(result)

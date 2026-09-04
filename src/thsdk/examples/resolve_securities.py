import thsdk

thsdk.auth()
result = thsdk.resolve_securities(codes=["300033", "600519"])
print(result)

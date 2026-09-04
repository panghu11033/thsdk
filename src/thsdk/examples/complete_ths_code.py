import thsdk

thsdk.auth()
result = thsdk.complete_ths_code(["300033", "600519"])
print(result)

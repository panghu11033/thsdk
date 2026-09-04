import thsdk

thsdk.auth()
result = thsdk.list_security_k_lines(
    security="USHA600519",
    start=-10,
    end=0,
    adjust=thsdk.Adjust.FORWARD,
    period=thsdk.Period.DAY,
)
print(result)

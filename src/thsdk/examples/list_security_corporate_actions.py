import thsdk

thsdk.auth()
result = thsdk.list_security_corporate_actions(
    security="USHA600519",
    start=-10,
    end=0,
    adjust=thsdk.Adjust.NONE,
    period=thsdk.Period.DAY,
)
print(result)

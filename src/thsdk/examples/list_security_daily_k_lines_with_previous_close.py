import thsdk

thsdk.auth()
result = thsdk.list_security_daily_k_lines_with_previous_close(
    security="USHA600519",
    start=-10,
    end=0,
    adjust=thsdk.Adjust.NONE,
)
print(result)

import thsdk

thsdk.auth()
result = thsdk.analyze_security_limit_up(
    security="USHA600519",
    date="2026-09-02T09:15:00+08:00",
)
print(result)

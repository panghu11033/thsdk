import thsdk

thsdk.auth()
result = thsdk.list_security_news_events(
    security="USHA600519",
    timeline="historical",
    window={
        "start": "2026-08-01T00:00:00+08:00",
        "end": "2026-09-02T23:59:59+08:00",
    },
)
print(result)

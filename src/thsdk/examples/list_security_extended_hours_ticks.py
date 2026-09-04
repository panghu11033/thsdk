import thsdk

thsdk.auth()
result = thsdk.list_security_extended_hours_ticks(
    security="UNQQAAPL",
    session="pre_market",
    window={
        "start": "2026-09-02T04:00:00-04:00",
        "end": "2026-09-02T09:30:00-04:00",
    },
)
print(result)

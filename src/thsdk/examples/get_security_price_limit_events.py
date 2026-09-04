import thsdk

thsdk.auth()
result = thsdk.get_security_price_limit_events(
    security="USHA600519",
    start_year=2025,
    end_year=2026,
)
print(result)

import thsdk

thsdk.auth()
result = thsdk.list_market_short_term_events(
    market="USHA",
    mode="security_scoped",
    securities=["USHA600519"],
    max_count=10,
)
print(result)

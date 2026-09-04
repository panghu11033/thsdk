import thsdk

thsdk.auth()
result = thsdk.list_security_extended_hours_intraday_bars(
    security="UNQQAAPL",
    session="pre_market",
    date="0",
)
print(result)

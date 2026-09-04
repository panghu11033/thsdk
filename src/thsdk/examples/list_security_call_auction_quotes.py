import thsdk

thsdk.auth()
result = thsdk.list_security_call_auction_quotes(
    security="USZA300033",
    phase="opening",
    date="2026-09-03T09:15:00+08:00",
)
print(result)

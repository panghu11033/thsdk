import thsdk

thsdk.auth()
result = thsdk.list_market_call_auction_unusual_events(
    market="USHA",
    trade_date="20260902",
)
print(result)

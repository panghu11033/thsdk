import thsdk

thsdk.auth()
result = thsdk.list_index_call_auction_quotes(
    index={
        "security": {"market": "USHI", "code": "1A0001"},
        "name": "上证指数",
    },
    phase="opening",
)
print(result)

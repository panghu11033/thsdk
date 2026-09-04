import thsdk

thsdk.auth()
result = thsdk.resolve_wencai_securities(
    query="市盈率小于20",
    limit=10,
)
print(result)

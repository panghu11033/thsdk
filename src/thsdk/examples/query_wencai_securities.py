import thsdk

thsdk.auth()
result = thsdk.query_wencai_securities(
    query="市盈率小于20",
    markets=["USHA", "USZA"],
    limit=10,
)
print(result)

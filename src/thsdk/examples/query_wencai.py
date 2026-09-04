import thsdk

thsdk.auth()
result = thsdk.query_wencai(
    query="市盈率小于20且个股热度排名前100",
    markets=["USHA", "USZA"],
    limit=10,
)
print(result)

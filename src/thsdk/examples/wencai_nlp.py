import thsdk

thsdk.auth()
result = thsdk.wencai_nlp(
    "市盈率小于20",
    markets=["USHA", "USZA"],
    limit=10,
)
print(result)

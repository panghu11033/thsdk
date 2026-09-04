import thsdk

thsdk.auth()
result = thsdk.list_security_order_books(
    securities=["USHA600519", "USZA300033"],
    depth="5",
)
print(result)

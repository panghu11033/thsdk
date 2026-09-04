import thsdk

thsdk.auth()
result = thsdk.list_security_daily_capital_flows(
    securities=["USHA600519", "USZA300033"],
)
print(result)

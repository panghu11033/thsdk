import thsdk

thsdk.auth()
result = thsdk.list_security_financial_snapshots(
    securities=["USHA600519", "USZA300033"],
    fields=["total_shares", "float_shares", "net_asset_per_share"],
)
print(result)

import thsdk

QUERY = "市盈率小于20"
RISE_PERCENTAGE_FIELD = "199112"

thsdk.auth()

selection = thsdk.query_wencai_securities(
    query=QUERY,
    markets=["USHA", "USZA"],
    limit=20,
)
securities = [item["security"] for item in selection.get("items") or []]

print(f"问财条件：{QUERY}")
print(f"命中总数：{selection.get('total', 0)}，本次股票池：{len(securities)}")

if securities:
    ranking = thsdk.sort_securities(
        securities=securities,
        sort_begin=0,
        sort_count=10,
        sort_id=RISE_PERCENTAGE_FIELD,
        sort_order="D",
    )
    ranked_securities = [
        item["security"] for item in ranking.get("securities") or []
    ]
    snapshots = thsdk.list_security_financial_snapshots(
        securities=ranked_securities,
        fields=[
            thsdk.FinancialSnapshotField.TOTAL_SHARES,
            thsdk.FinancialSnapshotField.FLOAT_SHARES,
            thsdk.FinancialSnapshotField.NET_ASSET_PER_SHARE,
        ],
    )

    print("\n股票池涨幅排序：")
    for item in ranking.get("securities") or []:
        print(item["full_code"])
    print("\n排序结果的基本面快照：")
    print(snapshots)

import thsdk

thsdk.auth()
result = thsdk.query_wencai_realtime_fields(
    securities=["USHA600519", "USZA300033"],
    fields=[
        {
            "query_group": "换手率",
            "query_key": "换手率",
            "index_name": "换手率",
            "show_name": "换手率",
            "timestamp": "20260902",
            "index": 2,
            "unit": "%",
            "type": "DOUBLE",
        }
    ],
)
print(result)

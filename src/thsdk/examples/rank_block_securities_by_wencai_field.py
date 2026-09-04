import thsdk

thsdk.auth()
result = thsdk.rank_block_securities_by_wencai_field(
    block=61322,
    field={
        "query_group": "换手率",
        "query_key": "换手率",
        "index_name": "换手率",
        "show_name": "换手率",
        "timestamp": "20260902",
        "index": 2,
        "unit": "%",
        "type": "DOUBLE",
    },
    offset=0,
    limit=10,
    sort_order="D",
)
print(result)

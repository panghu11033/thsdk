import thsdk

thsdk.auth()
result = thsdk.rank_block_securities(
    block=61322,
    sort_begin=0,
    sort_count=10,
    sort_id="55",
    sort_order="D",
)
print(result)

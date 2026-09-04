import thsdk

thsdk.auth()
result = thsdk.list_block_constituents(
    block=61322,
    sort_begin=0,
    sort_count=10,
)
print(result)

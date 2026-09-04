import thsdk

thsdk.auth()
result = thsdk.rank_constituents_by_performance_contribution(
    code="1A0001",
    market="USHI",
    target="index",
    sort_id=2708,
    sort_order="D",
    sort_begin=0,
    sort_count=10,
    valid_begin=0,
    valid_end=0,
)
print(result)

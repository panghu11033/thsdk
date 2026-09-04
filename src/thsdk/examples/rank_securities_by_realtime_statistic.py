import thsdk

thsdk.auth()
result = thsdk.rank_securities_by_realtime_statistic(
    markets=["USHA", "USZA"],
    sort_by=thsdk.RealtimeStatsMetric.LIMIT_UP_STATE,
    sort_dir="D",
    sort_begin=0,
    sort_count=10,
)
print(result)

import thsdk

thsdk.auth()
result = thsdk.calculate_security_realtime_statistics(
    securities=["USZA300033", "USHA600519"],
    metrics=[
        thsdk.RealtimeStatsMetric.LIMIT_UP_STATE,
        thsdk.RealtimeStatsMetric.LIMIT_UP_TYPE,
    ],
)
print(result)

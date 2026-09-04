import thsdk

thsdk.auth()
result = thsdk.list_security_option_greeks(
    securities=["UIFBC29DE"],
    metrics=[
        thsdk.OptionGreeksMetric.IMPLIED_VOLATILITY,
        thsdk.OptionGreeksMetric.DELTA,
    ],
)
print(result)

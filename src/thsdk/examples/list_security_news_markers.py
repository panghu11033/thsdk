import thsdk

thsdk.auth()
result = thsdk.list_security_news_markers(
    security="USHA600519",
    timeline="historical",
)
print(result)

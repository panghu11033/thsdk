import thsdk

thsdk.auth()
result = thsdk.list_hot_event_news(
    block=885988,
    range="recent",
)
print(result)

import thsdk

thsdk.auth()
result = thsdk.list_hot_block_calendar_events()
print(result)

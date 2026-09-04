import thsdk

thsdk.auth()
_ = thsdk.get_account_watchlist_groups()
print("请求完成，返回内容未展示")

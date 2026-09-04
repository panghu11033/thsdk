import thsdk

thsdk.auth()
_ = thsdk.get_account_watchlist()
print("请求完成，返回内容未展示")

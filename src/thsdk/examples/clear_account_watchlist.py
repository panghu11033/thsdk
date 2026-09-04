import thsdk

# 写操作默认关闭；确认下面的参数后再改为 True。
EXECUTE = False

if EXECUTE:
    thsdk.auth()
    result = thsdk.clear_account_watchlist()
    print(result)

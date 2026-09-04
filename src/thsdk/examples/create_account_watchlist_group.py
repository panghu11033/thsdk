import thsdk

# 写操作默认关闭；确认下面的参数后再改为 True。
EXECUTE = False

if EXECUTE:
    thsdk.auth()
    result = thsdk.create_account_watchlist_group(
        name="THSDK 示例组",
        securities=["USHA600519"],
    )
    print(result)

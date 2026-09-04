import thsdk

# 写操作默认关闭；确认下面的参数后再改为 True。
EXECUTE = False

if EXECUTE:
    thsdk.auth()
    result = thsdk.rename_account_watchlist_group(
        group_id=1,
        name="THSDK 示例组",
    )
    print(result)

import thsdk

# 退出会删除当前目录的 account.session，默认关闭。
EXECUTE = False

if EXECUTE:
    thsdk.logout()
    print("已退出并删除当前目录的会话")

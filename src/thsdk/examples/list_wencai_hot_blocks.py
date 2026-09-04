import thsdk

thsdk.auth()
result = thsdk.list_wencai_hot_blocks(kind="concept")
print(result)

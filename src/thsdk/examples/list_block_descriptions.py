import thsdk

thsdk.auth()
result = thsdk.list_block_descriptions(blocks=[61322])
print(result)

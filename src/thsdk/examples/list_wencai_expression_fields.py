import thsdk

thsdk.auth()
result = thsdk.list_wencai_expression_fields("市盈率小于20")
print(result)

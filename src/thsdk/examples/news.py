import thsdk

thsdk.auth()
result = thsdk.news(page=1, page_size=10)
print(result)

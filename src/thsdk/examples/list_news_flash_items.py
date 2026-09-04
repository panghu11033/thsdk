import thsdk

thsdk.auth()
result = thsdk.list_news_flash_items(
    traversal="page",
    page=1,
    page_size=10,
)
print(result)

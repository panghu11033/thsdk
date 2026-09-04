import thsdk

thsdk.auth()
result = thsdk.list_industry_children(
    industry={"security": {"market": "URFI", "code": "881121"}},
)
print(result)

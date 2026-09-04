import thsdk

thsdk.auth()
result = thsdk.list_security_research_reports(
    security="USHA600519",
    traversal={"mode": "page"},
)
print(result)

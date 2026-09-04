import thsdk

thsdk.auth()
result = thsdk.list_security_time_and_sales_ticks(
    security="UCFSsc9999",
    count=10,
)
print(result)

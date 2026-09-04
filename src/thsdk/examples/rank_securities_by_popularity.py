import thsdk

thsdk.auth()
result = thsdk.rank_securities_by_popularity(type=1)
print(result)

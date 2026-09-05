import thsdk

thsdk.auth()

watchlist = thsdk.get_account_watchlist()
groups = thsdk.get_account_watchlist_groups()

securities = watchlist.to_dict("records")
group_items = groups.to_dict("records")

print(f"账号自选：{len(securities)} 只")
print(f"自选分组：{len(group_items)} 个")
for group in group_items:
    members = group.get("securities") or []
    print(f"- {group.get('name') or '未命名分组'}：{len(members)} 只")

if securities:
    print("\n第一只自选证券最近 5 条日 K：")
    print(thsdk.get_price(securities[0], count=5))
else:
    print("\n当前账号没有自选证券。")

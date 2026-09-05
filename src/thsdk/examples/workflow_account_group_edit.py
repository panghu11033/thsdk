import thsdk

EXECUTE = False
GROUP_NAME = "thsdk-example"
RENAMED_GROUP_NAME = "thsdk-example-renamed"
SECURITY = "USZA300033"

if not EXECUTE:
    print("这是账号写入示例；确认后将 EXECUTE 改为 True 再运行。")
else:
    thsdk.auth()

    before = thsdk.get_account_watchlist_groups()
    before_ids = {int(group_id) for group_id in before.index}
    created_id = None

    try:
        created = thsdk.create_account_watchlist_group(name=GROUP_NAME)
        created_groups = created.get("groups") or {}
        new_ids = {int(group_id) for group_id in created_groups} - before_ids
        if len(new_ids) != 1:
            raise RuntimeError("无法唯一确认本次新建的分组，已停止后续写入")

        created_id = new_ids.pop()
        print(f"已创建临时分组：{created_id}")

        thsdk.rename_account_watchlist_group(
            group_id=created_id,
            name=RENAMED_GROUP_NAME,
        )
        print(f"已重命名为：{RENAMED_GROUP_NAME}")

        thsdk.add_account_watchlist_group_securities(
            group_id=created_id,
            securities=[SECURITY],
        )
        current = thsdk.get_account_watchlist_groups()
        current_group = next(
            (
                row
                for row in current.to_dict("records")
                if int(row.get("id") or 0) == created_id
            ),
            {},
        )
        print(f"加入证券后：{len(current_group.get('securities') or [])} 只")

        thsdk.remove_account_watchlist_group_securities(
            group_id=created_id,
            securities=[SECURITY],
        )
        print("已移除示例证券")
    finally:
        if created_id is not None:
            thsdk.delete_account_watchlist_group(group_id=created_id)
            print("已删除本次创建的临时分组")

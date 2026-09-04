import thsdk

SECURITY = "USZA300033"
LEVEL_2_BLOCK = 0xCE5F  # URFI 二级行业名称目录
LEVEL_3_BLOCK = 0xC4B5  # URFA 三级行业名称目录
RISE_PERCENTAGE_FIELD = "199112"

thsdk.auth()

# 查询并按涨幅排列同花顺二级行业。
level_2_names = thsdk.list_block_constituents(
    block=LEVEL_2_BLOCK,
    sort_begin=0,
    sort_count=0,
    sort_id="55",
    sort_order="A",
)
level_2_name_by_code = {
    item["full_code"]: item.get("name", "") for item in level_2_names
}
level_2_ranking = thsdk.rank_block_securities(
    block=LEVEL_2_BLOCK,
    sort_begin=0,
    sort_count=10,
    sort_id=RISE_PERCENTAGE_FIELD,
    sort_order="D",
)
print("二级行业涨幅排行：")
for item in level_2_ranking.get("securities") or []:
    print(item["full_code"], level_2_name_by_code.get(item["full_code"], ""))

# 从个股所属二级行业继续展开三级行业。
mapping = thsdk.get_security_industry(security=SECURITY)
level_2_industry = mapping["industry"]
level_3_children = thsdk.list_industry_children(industry=level_2_industry)

level_3_names = thsdk.list_block_constituents(
    block=LEVEL_3_BLOCK,
    sort_begin=0,
    sort_count=0,
    sort_id="55",
    sort_order="A",
)
level_3_name_by_code = {
    item["full_code"]: item.get("name", "") for item in level_3_names
}

print(f"\n{SECURITY} 的二级行业：{level_2_industry.get('name', '')}")
print("下属三级行业：")
for child in level_3_children:
    print(child["full_code"], level_3_name_by_code.get(child["full_code"], ""))

# 选择第一个三级行业，解析板块并显示按涨幅排列的成分股。
if level_3_children:
    level_3_code = level_3_children[0]["full_code"]
    level_3_name = level_3_name_by_code[level_3_code]
    level_3_block = thsdk.resolve_block(name=level_3_name)

    member_names = thsdk.list_block_constituents(
        block=level_3_block,
        sort_begin=0,
        sort_count=0,
        sort_id="55",
        sort_order="A",
    )
    member_name_by_code = {
        item["full_code"]: item.get("name", "") for item in member_names
    }
    member_ranking = thsdk.rank_block_securities(
        block=level_3_block,
        sort_begin=0,
        sort_count=10,
        sort_id=RISE_PERCENTAGE_FIELD,
        sort_order="D",
    )

    print(f"\n三级行业“{level_3_name}”成分股涨幅排行：")
    for item in member_ranking.get("securities") or []:
        print(item["full_code"], member_name_by_code.get(item["full_code"], ""))

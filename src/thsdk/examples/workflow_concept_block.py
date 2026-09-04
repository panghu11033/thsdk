import thsdk

RISE_PERCENTAGE_FIELD = "199112"

thsdk.auth()

# 热门概念给出发现顺序；再按名称解析可查询成分股的标准板块 ID。
hot = thsdk.list_wencai_hot_blocks(kind=thsdk.WencaiHotBlockKind.CONCEPT)
print("热门概念：")
for item in (hot.get("items") or [])[:5]:
    print(item["order"], item["block"]["name"], item.get("hot_tag", ""))

items = hot.get("items") or []
if items:
    concept_name = items[0]["block"]["name"]
    block = thsdk.resolve_block(name=concept_name)
    descriptions = thsdk.list_block_descriptions(blocks=[block])

    member_names = thsdk.list_block_constituents(
        block=block,
        sort_begin=0,
        sort_count=0,
        sort_id="55",
        sort_order="A",
    )
    member_name_by_code = {
        item["full_code"]: item.get("name", "") for item in member_names
    }
    ranking = thsdk.rank_block_securities(
        block=block,
        sort_begin=0,
        sort_count=10,
        sort_id=RISE_PERCENTAGE_FIELD,
        sort_order="D",
    )

    print(f"\n概念板块：{block['name']}")
    if descriptions:
        print("简介：", descriptions[0].get("description", ""))
    print("成分股涨幅排行：")
    for item in ranking.get("securities") or []:
        print(item["full_code"], member_name_by_code.get(item["full_code"], ""))

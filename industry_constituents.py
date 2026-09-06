"""导出同花顺二级行业及其成分股（适用于 THSDK 2.x）。"""

from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

import thsdk


INDUSTRY_DIRECTORY_BLOCK = 0xCE5F
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "data" / "industry_constituents.csv"


def full_code(item: Mapping[str, Any]) -> str:
    """从 Canonical API 返回项中取得完整证券代码。"""

    value = str(item.get("full_code") or "").strip()
    if value:
        return value

    security = item.get("security")
    if not isinstance(security, Mapping):
        return ""

    market = str(security.get("market") or "").strip()
    code = str(security.get("code") or "").strip()
    return f"{market}{code}" if market and code else code


def constituent_code_sort_key(value: str) -> tuple[str, str]:
    """按短代码排序，完整代码的四字符市场前缀用于消除同码歧义。"""

    if len(value) > 4:
        return value[4:], value[:4]
    return value, ""


def load_industries(limit: int | None = None) -> list[dict[str, Any]]:
    """取得同花顺二级行业目录。"""

    rows = thsdk.list_block_constituents(
        block=INDUSTRY_DIRECTORY_BLOCK,
        sort_begin=0,
        sort_count=0,
        sort_id="55",
        sort_order="A",
    )
    industries = rows.to_dict(orient="records")
    return industries[:limit] if limit is not None else industries


def load_constituents(industry: Mapping[str, Any]) -> list[dict[str, Any]]:
    """按行业证券身份取得该行业的全部关联成分股。"""

    security = industry.get("security")
    if not isinstance(security, Mapping):
        raise ValueError(f"行业缺少 security 身份：{industry!r}")

    result = thsdk.rank_related_securities(
        security=security,
        sort_begin=0,
        sort_count=0,
        sort_id="55",
        sort_order="A",
    )
    members = result.to_dict(orient="records")

    metadata = result.attrs.get("thsdk", {}).get("metadata", {})
    total_count = metadata.get("total_count") if isinstance(metadata, Mapping) else None
    if isinstance(total_count, int) and total_count >= 0 and len(members) != total_count:
        raise RuntimeError(
            f"服务端声明有 {total_count} 只成分股，本次只返回 {len(members)} 只"
        )
    return members


def export_industry_constituents(
    output: Path,
    *,
    delay: float = 0.5,
    limit: int | None = None,
) -> tuple[pd.DataFrame, list[str]]:
    """查询行业成分并写入汇总 CSV，返回结果和失败信息。"""

    print("正在认证……")
    thsdk.auth()

    industries = load_industries(limit)
    print(f"找到 {len(industries)} 个行业。")

    summaries: list[dict[str, Any]] = []
    failures: list[str] = []

    for index, industry in enumerate(industries, start=1):
        industry_code = full_code(industry)
        industry_name = str(industry.get("name") or "").strip()
        label = f"{industry_name} ({industry_code})"

        try:
            members = load_constituents(industry)
            member_codes = sorted(
                (code for item in members if (code := full_code(item))),
                key=constituent_code_sort_key,
            )
            summaries.append(
                {
                    "行业代码": industry_code,
                    "行业名称": industry_name,
                    "成分股数量": len(member_codes),
                    "成分股": ",".join(member_codes),
                }
            )
            print(f"[{index}/{len(industries)}] {label}: {len(member_codes)} 只")
        except Exception as exc:  # 单个行业失败时继续导出其他行业
            message = f"{label}: {exc}"
            failures.append(message)
            print(f"[{index}/{len(industries)}] {label}: 获取失败 - {exc}")

        if delay > 0 and index < len(industries):
            time.sleep(delay)

    result = pd.DataFrame(
        summaries,
        columns=("行业代码", "行业名称", "成分股数量", "成分股"),
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output, index=False, encoding="utf-8-sig")
    return result, failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"CSV 输出路径（默认：{DEFAULT_OUTPUT}）",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="每个行业之间的等待秒数（默认：0.5）",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="只处理前 N 个行业，适合快速试跑",
    )
    args = parser.parse_args()
    if args.delay < 0:
        parser.error("--delay 不能小于 0")
    if args.limit is not None and args.limit <= 0:
        parser.error("--limit 必须大于 0")
    return args


def main() -> int:
    args = parse_args()
    result, failures = export_industry_constituents(
        args.output,
        delay=args.delay,
        limit=args.limit,
    )

    print(f"\n已保存 {len(result)} 个行业到：{args.output.resolve()}")
    if not result.empty:
        print("\n结果预览：")
        print(result[["行业代码", "行业名称", "成分股数量"]].head().to_string(index=False))

    if failures:
        print(f"\n有 {len(failures)} 个行业获取失败：")
        for failure in failures:
            print(f"- {failure}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


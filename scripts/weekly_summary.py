#!/usr/bin/env python3
"""Aggregate the `分钟` column in daily logs and create a weekly draft."""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROW = re.compile(r"^\|\s*[^|]+\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成科研周报草稿")
    parser.add_argument("week", nargs="?", help="ISO 周，格式 YYYY-Www；默认本周")
    return parser.parse_args()


def week_dates(label: str) -> set[date]:
    match = re.fullmatch(r"(\d{4})-W(\d{2})", label)
    if not match:
        raise SystemExit("周格式应为 YYYY-Www，例如 2026-W32")
    year, week = map(int, match.groups())
    monday = date.fromisocalendar(year, week, 1)
    return {date.fromordinal(monday.toordinal() + offset) for offset in range(7)}


def collect(days: set[date]) -> tuple[dict[str, int], dict[str, int]]:
    by_project: dict[str, int] = defaultdict(int)
    by_type: dict[str, int] = defaultdict(int)
    for day in days:
        path = ROOT / "daily" / f"{day:%Y}" / f"{day:%m}" / f"{day:%F}.md"
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            match = ROW.match(line)
            if not match:
                continue
            minutes, project, activity = match.groups()
            by_project[project.strip()] += int(minutes)
            by_type[activity.strip()] += int(minutes)
    return dict(by_project), dict(by_type)


def duration(minutes: int) -> str:
    return f"{minutes // 60} h {minutes % 60:02d} min"


def make_table(by_project: dict[str, int], by_type: dict[str, int]) -> str:
    total = sum(by_project.values())
    lines = ["### 按项目", "", "| 项目 | 用时 | 占比 |", "|---|---:|---:|"]
    if total:
        for name, minutes in sorted(by_project.items(), key=lambda item: -item[1]):
            lines.append(f"| {name} | {duration(minutes)} | {minutes / total:.1%} |")
        lines.append(f"| **合计** | **{duration(total)}** | **100%** |")
    else:
        lines.append("| 暂无可统计记录 | 0 h 00 min | — |")

    lines += ["", "### 按活动类型", "", "| 类型 | 用时 |", "|---|---:|"]
    for name, minutes in sorted(by_type.items(), key=lambda item: -item[1]):
        lines.append(f"| {name} | {duration(minutes)} |")
    if not by_type:
        lines.append("| 暂无可统计记录 | 0 h 00 min |")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    today = date.today()
    label = args.week or f"{today.isocalendar().year}-W{today.isocalendar().week:02d}"
    by_project, by_type = collect(week_dates(label))
    template = (ROOT / "templates" / "weekly.md").read_text(encoding="utf-8")
    output = ROOT / "weekly" / f"{label}.md"
    if output.exists():
        raise SystemExit(f"周报已存在，未覆盖：{output.relative_to(ROOT)}")
    output.write_text(
        template.replace("{{WEEK}}", label).replace("{{TIME_TABLE}}", make_table(by_project, by_type)),
        encoding="utf-8",
    )
    print(f"已创建：{output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()


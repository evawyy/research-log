#!/usr/bin/env python3
"""Create a daily research log from the template."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="创建每日日志")
    parser.add_argument("date", nargs="?", help="日期，格式 YYYY-MM-DD；默认今天")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_date = date.fromisoformat(args.date) if args.date else date.today()
    output = ROOT / "daily" / f"{target_date:%Y}" / f"{target_date:%m}" / f"{target_date:%F}.md"

    if output.exists():
        print(f"日志已存在：{output.relative_to(ROOT)}")
        return

    template = (ROOT / "templates" / "daily.md").read_text(encoding="utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(template.replace("{{DATE}}", target_date.isoformat()), encoding="utf-8")
    print(f"已创建：{output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()


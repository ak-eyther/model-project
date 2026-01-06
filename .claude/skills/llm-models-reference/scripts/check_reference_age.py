#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path


def main() -> int:
    skill_dir = Path(__file__).resolve().parents[1]
    ref_path = skill_dir / "references" / "llm-models.md"
    if not ref_path.exists():
        print("Reference file not found: references/llm-models.md")
        return 1

    text = ref_path.read_text(encoding="utf-8")
    match = re.search(r"Last Updated:\s*(\d{4}-\d{2}-\d{2})", text)
    if not match:
        print("Last Updated date not found in reference")
        return 1

    updated = date.fromisoformat(match.group(1))
    age_days = (date.today() - updated).days

    print(f"Last Updated: {updated.isoformat()}")
    print(f"Age (days): {age_days}")
    if age_days > 30:
        print("Reference is older than 30 days; verify before critical decisions.")

    return 0


if __name__ == "__main__":
    sys.exit(main())

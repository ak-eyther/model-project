#!/usr/bin/env python3
"""Print a DPPM plan template for a feature/fix/refactor."""
from __future__ import annotations

import argparse
import re
import sys


def slugify(value: str) -> tuple[str, bool]:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value)
    slug = value.strip("-")
    if not slug:
        return "feature-plan", True
    return slug, False


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a DPPM plan template.")
    parser.add_argument("--feature", required=True, help="Feature name for the plan.")
    parser.add_argument(
        "--type",
        choices=["feature", "fix", "refactor"],
        default="feature",
        help="Type of work.",
    )
    args = parser.parse_args()

    feature_name = args.feature.strip()
    plan_slug, used_default = slugify(feature_name)
    plan_path = f"plans/{plan_slug}.md"
    if used_default:
        print(
            "Warning: feature name produced an empty slug; using 'feature-plan'.",
            file=sys.stderr,
        )

    print(f"Plan file: {plan_path}")
    print("")
    print(f"# {feature_name} Plan")
    print("")
    print("## Type")
    print(f"- {args.type}")
    print("")
    print("## Summary")
    print("- What this is")
    print("- Why we are doing it")
    print("")
    print("## Scope")
    print("- In scope:")
    print("- Out of scope:")
    print("")
    print("## Impact analysis")
    print("- Files/modules to touch:")
    print("  - UI:")
    print("  - API:")
    print("  - DB:")
    print("  - Infra:")
    print("  - Tests:")
    print("- Dependencies:")
    print("- Risks:")
    print("")
    print("## ASCII impact diagram")
    print("```")
    print("[Client/UI] --> [API] --> [DB]")
    print("      |             |")
    print("      v             v")
    print("  [components/]  [routes/]")
    print("```")
    print("")
    print("## Plan")
    print("### 1) <Major action item>")
    print("- [ ] <task>")
    print("- [ ] <task>")
    print("")
    print("### 2) <Major action item>")
    print("- [ ] <task>")
    print("- [ ] <task>")
    print("")
    print("### 3) <Major action item>")
    print("- [ ] <task>")
    print("- [ ] <task>")
    print("")
    print("## Evidence log")
    print("- Item 1: <evidence>")
    print("- Item 2: <evidence>")
    print("")
    print("## Compaction checkpoint")
    print("- Before compaction: update this plan with completed tasks and evidence.")
    print("- After compaction: reopen this plan and resume from the last evidenced item.")
    print("")
    print("## User test plan")
    print("- Test goal:")
    print("- Preconditions:")
    print("- Steps:")
    print("  1)")
    print("  2)")
    print("  3)")
    print("- Expected results:")
    print("- Pass criteria:")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fetch available models from Anthropic API.

Usage:
    python fetch_anthropic_models.py

Environment:
    ANTHROPIC_API_KEY: Required Anthropic API key
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Auto-load .env from backend directory
try:
    from dotenv import load_dotenv
    backend_env = Path(__file__).resolve().parents[4] / "backend" / ".env"
    if backend_env.exists():
        load_dotenv(backend_env)
except ImportError:
    pass


def main() -> int:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-key'")
        return 1

    try:
        from anthropic import Anthropic
    except ImportError:
        print("Error: anthropic package not installed")
        print("Install with: pip install anthropic")
        return 1

    client = Anthropic(api_key=api_key)

    print(f"Fetching Anthropic models... ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    print("=" * 60)

    try:
        # List all models
        models = client.models.list()

        # Group by model family
        families = {
            "claude-opus": [],
            "claude-sonnet": [],
            "claude-haiku": [],
            "claude-3": [],
            "other": [],
        }

        for model in models.data:
            model_id = model.id
            display_name = getattr(model, "display_name", model_id)
            created = getattr(model, "created_at", "N/A")

            info = {
                "id": model_id,
                "display_name": display_name,
                "created": created,
            }

            # Categorize
            if "opus" in model_id.lower():
                families["claude-opus"].append(info)
            elif "sonnet" in model_id.lower():
                families["claude-sonnet"].append(info)
            elif "haiku" in model_id.lower():
                families["claude-haiku"].append(info)
            elif "claude-3" in model_id.lower():
                families["claude-3"].append(info)
            else:
                families["other"].append(info)

        # Print organized output
        for family, model_list in families.items():
            if model_list:
                print(f"\n## {family.upper()} Models ({len(model_list)})")
                for m in sorted(model_list, key=lambda x: x["id"]):
                    print(f"  - {m['id']}")
                    if m["display_name"] != m["id"]:
                        print(f"    Display: {m['display_name']}")
                    if m["created"] != "N/A":
                        print(f"    Created: {m['created']}")

        total = sum(len(v) for v in families.values())
        print(f"\n{'=' * 60}")
        print(f"Total models: {total}")

    except Exception as e:
        print(f"Error fetching models: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

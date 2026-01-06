#!/usr/bin/env python3
"""Fetch available models from OpenAI API.

Usage:
    python fetch_openai_models.py

Environment:
    OPENAI_API_KEY: Required OpenAI API key
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Auto-load .env from repo root or backend directory (if present)
try:
    from dotenv import load_dotenv
    repo_root = Path(__file__).resolve().parents[4]
    candidate_envs = [
        repo_root / ".env",
        repo_root / "backend" / ".env",
    ]
    for env_path in candidate_envs:
        if env_path.exists():
            load_dotenv(env_path)
except ImportError:
    pass


def main() -> int:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Set it with: export OPENAI_API_KEY='your-key'")
        return 1

    try:
        from openai import OpenAI
    except ImportError:
        print("Error: openai package not installed")
        print("Install with: pip install openai")
        return 1

    client = OpenAI(api_key=api_key)

    print(f"Fetching OpenAI models... ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    print("=" * 60)

    try:
        models = client.models.list()

        # Group models by family
        families = {
            "gpt-5": [],
            "gpt-4": [],
            "gpt-3.5": [],
            "o1": [],
            "o3": [],
            "o4": [],
            "embedding": [],
            "whisper": [],
            "tts": [],
            "dall-e": [],
            "other": [],
        }

        for model in models.data:
            model_id = model.id
            categorized = False

            for family in families:
                if family in model_id.lower():
                    families[family].append(model_id)
                    categorized = True
                    break

            if not categorized:
                families["other"].append(model_id)

        # Print organized output
        for family, model_list in families.items():
            if model_list:
                print(f"\n## {family.upper()} Models ({len(model_list)})")
                for m in sorted(model_list):
                    print(f"  - {m}")

        print(f"\n{'=' * 60}")
        print(f"Total models: {len(models.data)}")

    except Exception as e:
        print(f"Error fetching models: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

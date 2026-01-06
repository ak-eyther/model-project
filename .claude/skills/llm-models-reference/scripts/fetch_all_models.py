#!/usr/bin/env python3
"""Fetch available models from all LLM providers (OpenAI + Anthropic).

Usage:
    python fetch_all_models.py [--json] [--update-reference]

Options:
    --json              Output as JSON instead of formatted text
    --update-reference  Update the llm-models.md reference file

Environment:
    OPENAI_API_KEY: OpenAI API key (optional, skips if not set)
    ANTHROPIC_API_KEY: Anthropic API key (optional, skips if not set)

Note: Auto-loads from backend/.env if python-dotenv is installed.
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
    pass  # dotenv not installed, rely on environment variables


def fetch_openai_models() -> dict:
    """Fetch models from OpenAI API."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"error": "OPENAI_API_KEY not set", "models": []}

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        models = client.models.list()

        return {
            "provider": "OpenAI",
            "fetched_at": datetime.now().isoformat(),
            "models": [
                {
                    "id": m.id,
                    "created": m.created,
                    "owned_by": m.owned_by,
                }
                for m in models.data
            ],
        }
    except ImportError:
        return {"error": "openai package not installed", "models": []}
    except Exception as e:
        return {"error": str(e), "models": []}


def fetch_anthropic_models() -> dict:
    """Fetch models from Anthropic API."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return {"error": "ANTHROPIC_API_KEY not set", "models": []}

    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        models = client.models.list()

        return {
            "provider": "Anthropic",
            "fetched_at": datetime.now().isoformat(),
            "models": [
                {
                    "id": m.id,
                    "display_name": getattr(m, "display_name", m.id),
                    "created_at": getattr(m, "created_at", None),
                }
                for m in models.data
            ],
        }
    except ImportError:
        return {"error": "anthropic package not installed", "models": []}
    except Exception as e:
        return {"error": str(e), "models": []}


def format_output(results: dict) -> str:
    """Format results for human-readable output."""
    lines = []
    lines.append("=" * 70)
    lines.append(f"LLM MODELS REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 70)

    for provider, data in results.items():
        lines.append(f"\n## {provider.upper()}")

        if "error" in data:
            lines.append(f"  Error: {data['error']}")
            continue

        models = data.get("models", [])
        lines.append(f"  Total: {len(models)} models")

        # Group by family
        if provider == "openai":
            families = {"gpt-5": [], "gpt-4": [], "o1": [], "o3": [], "o4": [], "embedding": [], "other": []}
            for m in models:
                mid = m["id"].lower()
                categorized = False
                for fam in ["gpt-5", "gpt-4", "o1", "o3", "o4", "embedding"]:
                    if fam in mid:
                        families[fam].append(m["id"])
                        categorized = True
                        break
                if not categorized:
                    families["other"].append(m["id"])

            for fam, mlist in families.items():
                if mlist and fam != "other":
                    lines.append(f"\n  ### {fam.upper()} ({len(mlist)})")
                    for mid in sorted(mlist)[:10]:  # Show top 10
                        lines.append(f"    - {mid}")
                    if len(mlist) > 10:
                        lines.append(f"    ... and {len(mlist) - 10} more")

        elif provider == "anthropic":
            families = {"opus": [], "sonnet": [], "haiku": [], "other": []}
            for m in models:
                mid = m["id"].lower()
                categorized = False
                for fam in ["opus", "sonnet", "haiku"]:
                    if fam in mid:
                        families[fam].append(m["id"])
                        categorized = True
                        break
                if not categorized:
                    families["other"].append(m["id"])

            for fam, mlist in families.items():
                if mlist:
                    lines.append(f"\n  ### {fam.upper()} ({len(mlist)})")
                    for mid in sorted(mlist):
                        lines.append(f"    - {mid}")

    lines.append("\n" + "=" * 70)
    return "\n".join(lines)


def main() -> int:
    args = sys.argv[1:]
    output_json = "--json" in args
    update_ref = "--update-reference" in args

    print("Fetching models from all providers...")

    results = {
        "openai": fetch_openai_models(),
        "anthropic": fetch_anthropic_models(),
    }

    if output_json:
        print(json.dumps(results, indent=2, default=str))
    else:
        print(format_output(results))

    if update_ref:
        ref_path = Path(__file__).resolve().parents[1] / "references" / "llm-models.md"
        if ref_path.exists():
            print(f"\nReference file: {ref_path}")
            print("Note: Auto-update not implemented. Review output and update manually.")
        else:
            print(f"\nWarning: Reference file not found at {ref_path}")

    # Return error if both providers failed
    if "error" in results["openai"] and "error" in results["anthropic"]:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

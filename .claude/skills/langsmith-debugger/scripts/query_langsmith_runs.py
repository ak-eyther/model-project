#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from typing import Any

import requests

DEFAULT_ENDPOINT = "https://api.smith.langchain.com"
DEFAULT_TENANT_ID = "81b6468e-dacf-403c-8cd6-b9b672b12836"
DEFAULT_PROJECT_ID = "092619fa-b4af-4543-8253-2903027dd7c5"


def _env(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)


def _require(name: str) -> str:
    value = _env(name)
    if not value:
        print(f"Missing required env var: {name}")
        raise SystemExit(1)
    return value


def _print_run(run: dict[str, Any]) -> None:
    run_id = run.get("id", "unknown")
    name = run.get("name", "unknown")
    status = run.get("status", "unknown")
    latency = run.get("latency", run.get("latency_ms"))
    latency_str = f"{latency}ms" if latency is not None else "n/a"
    print(f"{run_id[:8]} {status:<8} {latency_str:<8} {name}")


def main() -> int:
    endpoint = _env("LANGSMITH_ENDPOINT", DEFAULT_ENDPOINT).rstrip("/")
    api_key = _require("LANGSMITH_API_KEY")
    tenant_id = _env("LANGSMITH_TENANT_ID") or _env("LANGSMITH_WORKSPACE_ID") or DEFAULT_TENANT_ID
    project_id = _env("LANGSMITH_PROJECT_ID") or _env("LANGSMITH_SESSION_ID") or DEFAULT_PROJECT_ID
    limit = int(_env("LANGSMITH_LIMIT", "20"))
    filter_str = _env("LANGSMITH_FILTER")

    payload: dict[str, Any] = {"session": [project_id], "limit": limit}
    if filter_str:
        payload["filter"] = filter_str

    headers = {
        "x-api-key": api_key,
        "X-Tenant-ID": tenant_id,
        "Content-Type": "application/json",
    }

    url = f"{endpoint}/runs/query"
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        return 1

    if not response.ok:
        print(f"HTTP {response.status_code}: {response.text[:200]}")
        return 1

    data = response.json()
    runs = data.get("runs", [])
    print(f"Runs returned: {len(runs)}")
    for run in runs:
        _print_run(run)

    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from typing import Any

import requests

DEFAULT_BASE_URL = "https://sentry.io/api/0"
DEFAULT_ORG = "zappian-media"
DEFAULT_PROJECT = "python-serverless"
DEFAULT_QUERY = "is:unresolved"


def _env(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)


def _require(name: str) -> str:
    value = _env(name)
    if not value:
        print(f"Missing required env var: {name}")
        raise SystemExit(1)
    return value


def _print_issue(issue: dict[str, Any]) -> None:
    title = issue.get("title", "")[:80]
    count = issue.get("count", "?")
    last_seen = issue.get("lastSeen", "?")
    link = issue.get("permalink", "")
    print(f"{count:>6}  {last_seen:<20}  {title}")
    if link:
        print(f"        {link}")


def main() -> int:
    token = _require("SENTRY_AUTH_TOKEN")
    base_url = _env("SENTRY_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    org = _env("SENTRY_ORG", DEFAULT_ORG)
    project = _env("SENTRY_PROJECT", DEFAULT_PROJECT)
    query = _env("SENTRY_QUERY", DEFAULT_QUERY)
    limit = int(_env("SENTRY_LIMIT", "10"))

    headers = {"Authorization": f"Bearer {token}"}
    url = f"{base_url}/projects/{org}/{project}/issues/"

    try:
        response = requests.get(url, headers=headers, params={"query": query, "limit": limit}, timeout=30)
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        return 1

    if not response.ok:
        print(f"HTTP {response.status_code}: {response.text[:200]}")
        return 1

    issues = response.json()
    print(f"Issues returned: {len(issues)}")
    for issue in issues:
        _print_issue(issue)

    return 0


if __name__ == "__main__":
    sys.exit(main())

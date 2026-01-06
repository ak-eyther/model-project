#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from typing import Any

import requests

DEFAULT_BASE_URL = "https://sentry.io/api/0"


def _env(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)


def _require(name: str) -> str:
    value = _env(name)
    if not value:
        print(f"Missing required env var: {name}")
        raise SystemExit(1)
    return value


def _print_issue(issue: dict[str, Any]) -> None:
    print(f"Title: {issue.get('title', '')}")
    print(f"Status: {issue.get('status', '')}")
    print(f"Level: {issue.get('level', '')}")
    print(f"Count: {issue.get('count', '')}")
    print(f"Users: {issue.get('userCount', '')}")
    print(f"First Seen: {issue.get('firstSeen', '')}")
    print(f"Last Seen: {issue.get('lastSeen', '')}")
    print(f"Permalink: {issue.get('permalink', '')}")


def _print_latest_exception(event: dict[str, Any]) -> None:
    entries = event.get("entries", [])
    for entry in entries:
        if entry.get("type") != "exception":
            continue
        values = entry.get("data", {}).get("values", [])
        if not values:
            continue
        exc = values[-1]
        exc_type = exc.get("type", "")
        exc_value = exc.get("value", "")
        print("\nLatest Exception:")
        print(f"  {exc_type}: {exc_value}")
        frames = exc.get("stacktrace", {}).get("frames", [])
        if frames:
            print("  Stack (last 3 frames):")
            for frame in frames[-3:]:
                filename = frame.get("filename", "")
                line_no = frame.get("lineNo", "")
                func = frame.get("function", "")
                print(f"    {filename}:{line_no} in {func}")
        break


def main() -> int:
    token = _require("SENTRY_AUTH_TOKEN")
    issue_id = _require("SENTRY_ISSUE_ID")

    base_url = _env("SENTRY_BASE_URL", DEFAULT_BASE_URL).rstrip("/")

    headers = {"Authorization": f"Bearer {token}"}
    issue_url = f"{base_url}/issues/{issue_id}/"

    try:
        response = requests.get(issue_url, headers=headers, timeout=30)
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        return 1

    if not response.ok:
        print(f"HTTP {response.status_code}: {response.text[:200]}")
        return 1

    issue = response.json()
    _print_issue(issue)

    if _env("SENTRY_FETCH_LATEST_EVENT", "0") in {"1", "true", "yes"}:
        event_url = f"{base_url}/issues/{issue_id}/events/latest/"
        try:
            event_resp = requests.get(event_url, headers=headers, timeout=30)
        except requests.RequestException as exc:
            print(f"Event request failed: {exc}")
            return 1
        if event_resp.ok:
            _print_latest_exception(event_resp.json())
        else:
            print(f"Event HTTP {event_resp.status_code}: {event_resp.text[:200]}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

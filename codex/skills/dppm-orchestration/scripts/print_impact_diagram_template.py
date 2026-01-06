#!/usr/bin/env python3
"""Print ASCII impact diagram templates."""

def main() -> None:
    print("Example 1:")
    print("[UI] --> [API] --> [DB]")
    print(" |        |")
    print(" v        v")
    print("app/   backend/app/")
    print("")
    print("Example 2:")
    print("[Sidebar] ---> [Chat Page] ---> [Composer]")
    print("   |               |              |")
    print("components/      app/           components/")


if __name__ == "__main__":
    main()

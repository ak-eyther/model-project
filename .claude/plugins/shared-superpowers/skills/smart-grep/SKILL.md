---
name: smart-grep
description: Token-efficient codebase search using ripgrep with JSON output. Reduces token usage by 90-95% vs standard grep. Use for any codebase search to save tokens.
allowed-tools:
  - Bash
  - Read
---

# Smart Grep - Token-Efficient Search

## Quick Usage

```bash
rg --json "PATTERN" -t FILETYPE | python3 << 'EOF'
import json, sys
max_tokens = 10000
tokens = 0
for line in sys.stdin:
    try:
        data = json.loads(line)
    except:
        continue
    if data.get("type") != "match":
        continue
    path = data["data"]["path"]["text"]
    lnum = data["data"]["line_number"]
    text = data["data"]["lines"]["text"].rstrip()
    if len(text) > 300:
        text = text[:150] + " ... " + text[-150:]
    est_tokens = len((path + text).split()) * 1.3 + 10
    if tokens + est_tokens > max_tokens:
        break
    print(f"{path}:{lnum} {text}")
    tokens += est_tokens
EOF
```

## Examples

**Python files:**
```bash
rg --json "def authenticate" -t py | python3 << 'EOF'
[script above]
EOF
```

**TypeScript/React:**
```bash
rg --json "useState" -t ts -t tsx | python3 << 'EOF'
[script above]
EOF
```

## Token Budget

- Quick lookup: 5,000 tokens
- Normal search: 10,000 tokens (default)
- Deep search: 20,000 tokens

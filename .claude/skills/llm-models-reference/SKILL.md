---
name: llm-models-reference
description: Reference guide for LLM model IDs, capabilities, pricing, and provider endpoints. Use when selecting a model, comparing provider capabilities, or validating model IDs for {{PROJECT_NAME}}.
---

# LLM Models Reference

Use this skill as a pointer to the full reference document.

## Quick Start

- `python .claude/skills/llm-models-reference/scripts/check_reference_age.py`
- Read `references/llm-models.md` for model lineups, pricing, capability matrices, and API examples.

## Bundled Resources

### References
- `references/llm-models.md`: model IDs, pricing, capability matrices, API examples.

### Scripts
- `scripts/check_reference_age.py`: check last-updated age.
- `scripts/fetch_openai_models.py`: fetch current OpenAI models via API.
- `scripts/fetch_anthropic_models.py`: fetch current Anthropic models via API.
- `scripts/fetch_all_models.py`: fetch models from all providers (unified script).

## Fetching Latest Models

Requires API keys in environment:

```bash
# Set API keys
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# Fetch from all providers
python .claude/skills/llm-models-reference/scripts/fetch_all_models.py

# JSON output
python .claude/skills/llm-models-reference/scripts/fetch_all_models.py --json

# Single provider
python .claude/skills/llm-models-reference/scripts/fetch_openai_models.py
python .claude/skills/llm-models-reference/scripts/fetch_anthropic_models.py
```

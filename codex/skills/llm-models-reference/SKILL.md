---
name: llm-models-reference
description: Reference guide for OpenAI model IDs, capabilities, pricing, and provider endpoints. Use when selecting a model, comparing OpenAI capabilities, or validating model IDs for {{PROJECT_NAME}}.
---

# OpenAI Models Reference

Use this skill as a pointer to the full reference document.

**Project context:** Fill placeholders in this skill and the reference doc using `codex/PROJECT_CONTEXT.md`.

## Quick Start

- `python codex/skills/llm-models-reference/scripts/check_reference_age.py`
- Read `codex/skills/llm-models-reference/references/llm-models.md` for model lineups, pricing, capability matrices, and API examples.

## Bundled Resources

### References
- `references/llm-models.md`: OpenAI model IDs, pricing, capability matrices, API examples.

### Scripts
- `scripts/check_reference_age.py`: check last-updated age.
- `scripts/fetch_openai_models.py`: fetch current OpenAI models via API.

## Fetching Latest Models

Requires an OpenAI API key in the environment:

```bash
export OPENAI_API_KEY="sk-..."
python codex/skills/llm-models-reference/scripts/fetch_openai_models.py
```

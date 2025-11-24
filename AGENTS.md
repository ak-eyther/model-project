# Repository Guidelines

## Project Structure & Module Organization
- Core wizard: `setup.py` bootstraps projects and renders templates.
- Agent system: `.claude/agents/` holds markdown definitions; `.claude/scripts/` contains automation (init, structure validation, skill updates); `.claude/structure/` defines canonical layout; `.claude/memory/` stores agent memory JSON.
- Docs: `docs/` contains quick starts, tier comparison, and usage guides; `AGENT_COMMUNICATION_BOARD.md` and `CLAUDE.md` provide working context for agents.
- Tests: `tests/validate_setup.py` ensures hooks, structure, memory, and CLAUDE.md are correct.
- Templates: `templates/` and `*.j2` files power rendering; avoid leaving Jinja placeholders after generation.

## Build, Test, and Development Commands
- Initialize a new project instance:
  ```bash
  python setup.py
  ```
- Install/update git hooks:
  ```bash
  ./.claude/scripts/install-hooks.sh
  ```
- Validate structure and agent metadata:
  ```bash
  python .claude/scripts/structure_validator.py
  ./.claude/scripts/validate-agent-skills.sh
  ```
- Full setup check (preferred pre-PR gate):
  ```bash
  python tests/validate_setup.py
  ```

## Coding Style & Naming Conventions
- Python: follow PEP 8, prefer type hints and f-strings; keep scripts portable (no hardcoded paths); keep colors/emoji minimal in logic.
- Shell: start with `set -e`, quote variables, check command existence.
- Markdown: ATX headers, fenced code blocks with language tags; keep instructions concise.
- Branch names: `feature/<slug>` or `fix/<slug>`; agent files use kebab-case names (e.g., `.claude/agents/memory-expert.md`).

## Testing Guidelines
- Primary check: `python tests/validate_setup.py` (covers hooks, structure validator, memory files, CLAUDE.md).
- For script changes, run targeted validators in `.claude/scripts/` (structure, agent skills, context).
- Add new Python checks to `tests/` as `test_<topic>.py` and ensure they are executable with `python -m pytest` or direct invocation.

## Commit & Pull Request Guidelines
- Commit format: `[CATEGORY-ID] Description` (e.g., `[CHORE-102] Refresh hooks installer`).
- Keep commits scoped; include updates to docs/templates alongside code changes.
- PRs should summarize intent, list validation commands run, and link issues; attach screenshots only when UI artifacts change.
- Ensure generated files have no remaining `{{ }}` placeholders and that hooks remain executable (`chmod +x`) before requesting review.

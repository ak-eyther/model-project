# Canonical Structure Enforcement System

## Overview

The Canonical Structure Enforcement System maintains consistent file organization throughout the project through automated validation, repair, and cleanup. It ensures that all files are placed in their designated locations according to project conventions.

## Architecture

### Components

1. **Canonical Structure Schema** (`canonical-structure.yaml`)
   - Single source of truth for file placement rules
   - Defines patterns, locations, and lifecycle rules
   - Configurable enforcement settings

2. **Validation Engine** (`../scripts/structure-validator.py`)
   - Validates project structure against schema
   - Used by git hooks and auto-fix scripts
   - Returns violations with suggested corrections

3. **Auto-Fix Script** (`../scripts/auto-fix.py`)
   - Detects and corrects structure violations
   - Queries Memory Expert before moving files
   - Supports dry-run mode for safety

4. **Git Hooks** (`.git/hooks/pre-commit`)
   - Prevents commits with structure violations
   - Provides clear error messages and fix commands
   - Can be bypassed with `--no-verify` in emergencies

5. **Documentation Manager Agent** (`../agents/documentation-manager.md`)
   - Orchestrates nightly cleanup operations
   - Integrates with Memory Expert for safety checks
   - Archives completed work automatically

## Quick Start

### Installation

```bash
# Install git hooks (one-time setup)
.claude/scripts/install-hooks.sh

# Verify installation
ls -la .git/hooks/pre-commit
```

### Daily Workflow

1. **Normal Development**
   - Create and modify files as usual
   - Git hook validates structure on commit
   - If validation fails, run auto-fix

2. **Fixing Violations**
   ```bash
   # Check for violations (dry-run)
   .claude/scripts/auto-fix.py --dry-run

   # Apply fixes
   .claude/scripts/auto-fix.py --apply

   # Commit the fixes
   git add .
   git commit -m "chore: fix file structure violations"
   ```

3. **Manual Cleanup**
   ```bash
   # Run Documentation Manager manually
   python .claude/scripts/cleanup-manager.py --preview

   # Apply cleanup
   python .claude/scripts/cleanup-manager.py --apply
   ```

## File Type Rules

### Completion Reports
- **Pattern:** `*-COMPLETE*.md`, `*-COMPLETION*.md`
- **Location:** `.claude/archive/completion-reports/`
- **Lifecycle:** Archive after 7 days when task completed
- **Memory Expert:** Required for archival

### Impact Analysis
- **Pattern:** `*-impact-analysis.md`
- **Location:** `.claude/memory/impact-analysis/`
- **Lifecycle:** Archive after 30 days when feature completed
- **Archive To:** `.claude/archive/impact-analyses/`

### Agent Memory
- **Pattern:** `*-memory.json`, `*-calibration.json`
- **Location:** `.claude/memory/`
- **Lifecycle:** Never archived (permanent)

### Testing Artifacts
- **Pattern:** `test-*.log`, `*-test-results.md`
- **Location:** `.claude/archive/testing/`
- **Lifecycle:** Archive after 14 days

### Design Specifications
- **Pattern:** `*-DESIGN.md`, `*-spec.md`
- **Location:** `.claude/memory/design-specs/`
- **Lifecycle:** Archive after 45 days when implemented

## Configuration

### Enforcement Modes

1. **Warning Mode** (default)
   - Shows violations but allows commit
   - Recommended for initial rollout

2. **Strict Mode**
   - Blocks commits with violations
   - Use after team is familiar with system

3. **Disabled Mode**
   - No enforcement (emergency use only)

### Customization

Edit `canonical-structure.yaml` to:
- Add new file type rules
- Modify lifecycle policies
- Change retention periods
- Update enforcement settings

Example custom rule:
```yaml
file_types:
  - name: "custom_reports"
    patterns:
      - "CUSTOM-*.md"
    canonical_location: ".claude/custom/"
    lifecycle_rule:
      trigger: "file_age > 30 days"
      action: "archive"
```

## Troubleshooting

### Common Issues

**Issue:** Git hook blocks valid commit
```bash
# Emergency bypass
git commit --no-verify -m "emergency: bypass structure check"

# Then fix and recommit properly
```

**Issue:** Auto-fix moves wrong file
```bash
# Find the commit
git log --oneline | grep "auto-archive"

# Restore file
git checkout <commit>~1 -- path/to/file.md
```

**Issue:** Hook is too slow
```bash
# Clear cache
rm -rf .claude/structure/.cache/

# Hook will rebuild cache on next run
```

### Safety Features

1. **Archive-First Approach**
   - Never deletes files, only archives
   - All moves tracked in git history

2. **Memory Expert Integration**
   - Queries before archiving active files
   - Defaults to keeping files when uncertain

3. **Dry-Run Mode**
   - All scripts default to preview mode
   - Requires explicit `--apply` to make changes

4. **Environment Guards**
   - Prevents execution on production servers
   - Checks for Railway/Vercel environment variables

## Performance

- **Git Hook:** < 2 seconds for typical commit
- **Auto-Fix:** < 30 seconds for full project scan
- **Cleanup:** < 5 minutes for nightly run

Performance optimizations:
- Validation results cached for 5 minutes
- Only changed files validated on commit
- Batch processing for multiple files

## Security

- **Path Traversal Protection:** All paths validated against project root
- **Command Injection Protection:** Uses pathlib, no shell execution
- **Archive Strategy:** Always preserves data, never deletes

## Support

For issues or questions:
1. Check this README
2. Review error messages (usually contain fix commands)
3. Consult Memory Expert for file safety
4. Ask Documentation Manager agent for help

## Version History

- **v1.0.0** (2025-11-22): Initial implementation
  - Core structure enforcement
  - Git hook integration
  - Memory Expert integration
  - Documentation Manager agent

---

*Maintained by: Documentation Manager Agent*
*Last Updated: 2025-11-22*
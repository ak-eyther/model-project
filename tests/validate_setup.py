#!/usr/bin/env python3
"""
Setup Validation Script
Validates that the project was set up correctly
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Tuple

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
END = '\033[0m'

class SetupValidator:
    def __init__(self):
        self.project_root = Path.cwd()
        self.checks_passed = 0
        self.checks_failed = 0

    def run_all_checks(self) -> bool:
        """Run all validation checks"""
        print("\nRunning setup validation...\n")

        checks = [
            ("Git hooks installed", self.check_git_hooks),
            ("Structure validator operational", self.check_structure_validator),
            ("Agent frontmatter valid", self.check_agent_frontmatter),
            ("Memory system initialized", self.check_memory_files),
            ("CLAUDE.md configured", self.check_claude_md),
            ("Scripts executable", self.check_script_permissions),
            ("Configuration files valid", self.check_config_files),
        ]

        for name, check_fn in checks:
            try:
                check_fn()
                self.check_passed(name)
            except Exception as e:
                self.check_failed(name, str(e))

        print()
        if self.checks_failed == 0:
            print(f"{GREEN}🎉 All checks passed! Setup complete.{END}\n")
            return True
        else:
            print(f"{RED}⚠️  {self.checks_failed} checks failed.{END}\n")
            return False

    def check_passed(self, name: str):
        """Mark check as passed"""
        print(f"{GREEN}✅ {name}{END}")
        self.checks_passed += 1

    def check_failed(self, name: str, error: str):
        """Mark check as failed"""
        print(f"{RED}❌ {name}: {error}{END}")
        self.checks_failed += 1

    def check_git_hooks(self):
        """Verify git hooks are installed"""
        hooks_dir = self.project_root / '.git' / 'hooks'
        required_hooks = ['pre-commit', 'commit-msg', 'post-merge']

        if not hooks_dir.exists():
            raise Exception("Git hooks directory not found")

        for hook in required_hooks:
            hook_path = hooks_dir / hook
            if not hook_path.exists():
                raise Exception(f"{hook} not found")
            if not os.access(hook_path, os.X_OK):
                raise Exception(f"{hook} not executable")

    def check_structure_validator(self):
        """Verify structure validator exists and runs"""
        validator = self.project_root / '.claude/scripts/structure_validator.py'
        if not validator.exists():
            raise Exception("structure_validator.py not found")

        # Try to import it (basic syntax check)
        result = subprocess.run(
            ['python3', '-m', 'py_compile', str(validator)],
            capture_output=True
        )
        if result.returncode != 0:
            raise Exception("structure_validator.py has syntax errors")

    def check_agent_frontmatter(self):
        """Validate all agents have proper frontmatter"""
        agents_dir = self.project_root / '.claude/agents'
        if not agents_dir.exists():
            raise Exception("Agents directory not found")

        agent_files = list(agents_dir.glob('*.md'))
        if len(agent_files) == 0:
            raise Exception("No agent files found")

        required_fields = ['agent_name', 'permissionMode']

        for agent_file in agent_files:
            content = agent_file.read_text()

            if not content.startswith('---'):
                raise Exception(f"{agent_file.name} missing frontmatter")

            # Extract frontmatter
            parts = content.split('---')
            if len(parts) < 3:
                raise Exception(f"{agent_file.name} invalid frontmatter format")

            frontmatter = parts[1]

            for field in required_fields:
                if f'{field}:' not in frontmatter:
                    raise Exception(
                        f"{agent_file.name} missing required field: {field}"
                    )

    def check_memory_files(self):
        """Verify memory files were created"""
        memory_dir = self.project_root / '.claude/memory'
        if not memory_dir.exists():
            raise Exception("Memory directory not found")

        memory_files = list(memory_dir.glob('*-memory.json'))
        if len(memory_files) < 5:
            raise Exception(f"Only {len(memory_files)} memory files found (expected at least 5)")

        # Validate JSON structure
        for memory_file in memory_files[:3]:  # Check first 3
            with open(memory_file, 'r') as f:
                data = json.load(f)

            required_keys = ['agent_name', 'hot_memory', 'warm_memory', 'cold_memory']
            for key in required_keys:
                if key not in data:
                    raise Exception(f"{memory_file.name} missing key: {key}")

    def check_claude_md(self):
        """Verify CLAUDE.md exists and is configured"""
        claude_md = self.project_root / 'CLAUDE.md'
        if not claude_md.exists():
            raise Exception("CLAUDE.md not found")

        content = claude_md.read_text()

        # Check no Jinja2 placeholders remain
        if '{{' in content or '}}' in content:
            raise Exception("CLAUDE.md still contains Jinja2 placeholders")

        # Check has project-specific content
        if "Project Overview" not in content:
            raise Exception("CLAUDE.md missing Project Overview section")

    def check_script_permissions(self):
        """Verify scripts are executable"""
        scripts_dir = self.project_root / '.claude/scripts'
        if not scripts_dir.exists():
            raise Exception("Scripts directory not found")

        shell_scripts = list(scripts_dir.glob('*.sh'))
        if len(shell_scripts) == 0:
            raise Exception("No shell scripts found")

        for script in shell_scripts:
            if not os.access(script, os.X_OK):
                raise Exception(f"{script.name} not executable")

    def check_config_files(self):
        """Verify configuration files are valid"""
        config_dir = self.project_root / '.claude/config'
        if not config_dir.exists():
            raise Exception("Config directory not found")

        # Check project-config.yaml
        project_config = config_dir / 'project-config.yaml'
        if project_config.exists():
            import yaml
            with open(project_config, 'r') as f:
                data = yaml.safe_load(f)

            if 'project' not in data or 'tech_stack' not in data:
                raise Exception("project-config.yaml invalid structure")

        # Check reflection-config.json
        reflection_config = config_dir / 'reflection-config.json'
        if reflection_config.exists():
            with open(reflection_config, 'r') as f:
                data = json.load(f)

            if 'tier1_agents' not in data or 'tier2_validator' not in data:
                raise Exception("reflection-config.json invalid structure")

def main():
    validator = SetupValidator()
    success = validator.run_all_checks()

    if success:
        print("Next steps:")
        print("1. Read docs/QUICK_START_STANDARD.md")
        print("2. Invoke your first agent: @anand-2.0")
        print("3. Make a test commit to verify hooks\n")

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

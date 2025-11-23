#!/usr/bin/env python3
"""
Structure Validation Engine
Validates project structure against canonical rules defined in YAML schema
"""

import os
import sys
import json
import yaml
import hashlib
import argparse
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import fnmatch
from dataclasses import dataclass, asdict

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
STRUCTURE_DIR = PROJECT_ROOT / ".claude" / "structure"
CACHE_DIR = STRUCTURE_DIR / ".cache"
CANONICAL_STRUCTURE_FILE = STRUCTURE_DIR / "canonical-structure.yaml"
VALIDATION_RULES_FILE = STRUCTURE_DIR / "validation-rules.json"

@dataclass
class Violation:
    """Represents a structure violation"""
    file_path: str
    current_location: str
    canonical_location: str
    rule_name: str
    severity: str  # "error", "warning", "info"
    message: str
    fix_command: Optional[str] = None

class StructureValidator:
    """Main validation engine"""

    def __init__(self, config_file: Optional[Path] = None):
        self.config_file = config_file or CANONICAL_STRUCTURE_FILE
        self.config = self._load_config()
        self.cache = self._load_cache()
        self.violations: List[Violation] = []

    def _load_config(self) -> Dict[str, Any]:
        """Load canonical structure configuration"""
        if not self.config_file.exists():
            logger.error(f"Configuration file not found: {self.config_file}")
            sys.exit(1)

        try:
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML: {e}")
            sys.exit(1)

    def _load_cache(self) -> Dict[str, Any]:
        """Load validation cache from JSON"""
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file = CACHE_DIR / "validation_cache.json"

        if not cache_file.exists():
            return {}

        try:
            with open(cache_file, 'r') as f:
                cache = json.load(f)
                # Check cache TTL
                if cache.get('timestamp'):
                    timestamp = datetime.fromisoformat(cache['timestamp'])
                    age = datetime.now() - timestamp
                    ttl = self.config.get('settings', {}).get('cache_ttl_seconds', 300)
                    if age.total_seconds() > ttl:
                        return {}
                return cache
        except Exception as e:
            logger.warning(f"Failed to load cache: {e}")
            return {}

    def _save_cache(self):
        """Save validation cache as JSON"""
        cache_file = CACHE_DIR / "validation_cache.json"
        self.cache['timestamp'] = datetime.now().isoformat()

        try:
            with open(cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")

    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate file hash for cache invalidation"""
        if not file_path.exists():
            return ""
        return hashlib.md5(str(file_path.stat().st_mtime).encode()).hexdigest()

    def validate_structure(self, files: Optional[List[Path]] = None) -> List[Violation]:
        """Validate project structure"""
        self.violations = []

        # Get files to validate
        if files:
            # Validate specific files
            for file_path in files:
                if file_path.exists():
                    self._validate_file(file_path)
        else:
            # Validate entire project
            self._validate_all_files()

        # Check forbidden patterns
        self._check_forbidden_patterns()

        # Save cache
        if self.config.get('settings', {}).get('cache_validation_results', True):
            self._save_cache()

        return self.violations

    def _validate_file(self, file_path: Path):
        """Validate a single file"""
        # Skip if in .git or other ignored directories
        if self._should_ignore(file_path):
            return

        # Check cache
        cache_key = str(file_path.relative_to(PROJECT_ROOT))
        file_hash = self._get_file_hash(file_path)

        if cache_key in self.cache and self.cache[cache_key].get('hash') == file_hash:
            # Use cached result
            cached_violations = self.cache[cache_key].get('violations', [])
            for v_dict in cached_violations:
                self.violations.append(Violation(**v_dict))
            return

        # Find matching rule
        violations = []
        matched_rule = self._find_matching_rule(file_path)

        if matched_rule:
            canonical_location = matched_rule.get('canonical_location')
            if canonical_location and canonical_location != 'null':
                # Check if file is in canonical location
                expected_parent = PROJECT_ROOT / canonical_location
                actual_parent = file_path.parent

                if not self._is_in_location(file_path, canonical_location):
                    violation = Violation(
                        file_path=str(file_path),
                        current_location=str(actual_parent.relative_to(PROJECT_ROOT)),
                        canonical_location=canonical_location,
                        rule_name=matched_rule['name'],
                        severity="error" if self._is_strict_mode() else "warning",
                        message=f"File should be in {canonical_location}",
                        fix_command=f"git mv {file_path} {expected_parent / file_path.name}"
                    )
                    violations.append(violation)
                    self.violations.append(violation)

        # Update cache - convert Violation objects to dicts for JSON serialization
        self.cache[cache_key] = {
            'hash': file_hash,
            'violations': [asdict(v) for v in violations]
        }

    def _validate_all_files(self):
        """Validate all files in project"""
        for root, dirs, files in os.walk(PROJECT_ROOT):
            root_path = Path(root)

            # Skip ignored directories
            dirs[:] = [d for d in dirs if not self._should_ignore(root_path / d)]

            for file_name in files:
                file_path = root_path / file_name
                self._validate_file(file_path)

    def _find_matching_rule(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Find the rule that matches this file"""
        relative_path = file_path.relative_to(PROJECT_ROOT)
        file_name = file_path.name

        for file_type in self.config.get('file_types', []):
            # Check patterns
            for pattern in file_type.get('patterns', []):
                if fnmatch.fnmatch(file_name, pattern):
                    # Check additional conditions
                    conditions = file_type.get('conditions', [])
                    if self._check_conditions(file_path, conditions):
                        return file_type

        return None

    def _check_conditions(self, file_path: Path, conditions: List[str]) -> bool:
        """Check additional conditions for a rule"""
        if not conditions:
            return True

        for condition in conditions:
            if "parent_dir ==" in condition:
                expected_parent = condition.split("==")[1].strip().strip('"').strip("'")
                actual_parent = str(file_path.parent.relative_to(PROJECT_ROOT))
                if not actual_parent.endswith(expected_parent.strip("/")):
                    return False

        return True

    def _is_in_location(self, file_path: Path, canonical_location: str) -> bool:
        """Check if file is in or under the canonical location"""
        canonical_path = (PROJECT_ROOT / canonical_location).resolve()
        try:
            file_parent = file_path.resolve().parent
            # A file is "in location" if its parent is the canonical dir or any subdir under it
            return canonical_path == file_parent or canonical_path in file_parent.parents
        except Exception:
            return False

    def _check_forbidden_patterns(self):
        """Check for forbidden patterns in specific directories"""
        for forbidden in self.config.get('forbidden_patterns', []):
            location = PROJECT_ROOT / forbidden['location'].lstrip('/')
            if not location.exists():
                continue

            patterns = forbidden['patterns']
            exceptions = forbidden.get('exceptions', [])

            recursive = forbidden.get('recursive', True)

            for root, dirs, files in os.walk(location):
                if not recursive:
                    dirs[:] = []  # Do not descend into subdirectories
                root_path = Path(root)
                if self._should_ignore(root_path):
                    continue
                for file_name in files:
                    # Skip exceptions
                    if file_name in exceptions:
                        continue

                    # Check patterns
                    for pattern in patterns:
                        if fnmatch.fnmatch(file_name, pattern):
                            file_path = root_path / file_name
                            violation = Violation(
                                file_path=str(file_path),
                                current_location=str(root_path.relative_to(PROJECT_ROOT)),
                                canonical_location="[should be moved/deleted]",
                                rule_name="forbidden_pattern",
                                severity="error",
                                message=forbidden['message'],
                                fix_command=f"# Review and move: {file_path}"
                            )
                            self.violations.append(violation)

    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored"""
        ignore_dirs = {'.git', '.github', 'node_modules', '__pycache__',
                      '.pytest_cache', 'dist', 'build', '.next', '.DS_Store',
                      'backups'}

        for part in path.parts:
            if part in ignore_dirs:
                return True
        return False

    def _is_strict_mode(self) -> bool:
        """Check if enforcement is in strict mode"""
        return self.config.get('settings', {}).get('enforcement_mode') == 'strict'

    def format_violations(self, violations: List[Violation]) -> str:
        """Format violations for display"""
        if not violations:
            return "✅ No structure violations found!"

        output = ["❌ Structure violations detected:\n"]

        # Group by severity
        errors = [v for v in violations if v.severity == "error"]
        warnings = [v for v in violations if v.severity == "warning"]

        if errors:
            output.append(f"ERRORS ({len(errors)}):")
            for v in errors:
                output.append(f"  ❌ {Path(v.file_path).name}")
                output.append(f"     Current: {v.current_location}")
                output.append(f"     Should be: {v.canonical_location}")
                output.append(f"     Fix: {v.fix_command}")

        if warnings:
            output.append(f"\nWARNINGS ({len(warnings)}):")
            for v in warnings:
                output.append(f"  ⚠️  {Path(v.file_path).name}")
                output.append(f"     Current: {v.current_location}")
                output.append(f"     Should be: {v.canonical_location}")

        output.append(f"\n💡 To fix automatically, run:")
        output.append(f"   .claude/scripts/auto-fix.py --apply")

        return "\n".join(output)

def main():
    """Main entry point"""
    if sys.version_info < (3, 7):
        logger.error("Python 3.7+ is required for structure validation.")
        sys.exit(1)
    parser = argparse.ArgumentParser(description="Validate project structure")
    parser.add_argument('--mode', choices=['pre-commit', 'full', 'files'],
                       default='full', help='Validation mode')
    parser.add_argument('--files', nargs='+', help='Specific files to validate')
    parser.add_argument('--config', type=Path, help='Custom config file')
    parser.add_argument('--json', action='store_true', help='Output JSON format')
    parser.add_argument('--quiet', action='store_true', help='Minimal output')

    args = parser.parse_args()

    # Initialize validator
    validator = StructureValidator(config_file=args.config)

    # Force strict mode for pre-commit so violations block commits
    if args.mode == 'pre-commit':
        validator.config.setdefault('settings', {})['enforcement_mode'] = 'strict'

    # Get files to validate
    files = None
    if args.mode == 'pre-commit':
        # Get staged files from git
        import subprocess
        result = subprocess.run(['git', 'diff', '--cached', '--name-only'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            files = [PROJECT_ROOT / f for f in result.stdout.strip().split('\n') if f]
    elif args.files:
        files = [Path(f) for f in args.files]

    # Validate
    violations = validator.validate_structure(files=files)

    # Output results
    if args.json:
        output = json.dumps([{
            'file_path': v.file_path,
            'current_location': v.current_location,
            'canonical_location': v.canonical_location,
            'rule_name': v.rule_name,
            'severity': v.severity,
            'message': v.message,
            'fix_command': v.fix_command
        } for v in violations], indent=2)
        print(output)
    elif not args.quiet:
        print(validator.format_violations(violations))

    # Exit code
    if violations and validator._is_strict_mode():
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()

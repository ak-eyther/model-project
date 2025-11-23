#!/usr/bin/env python3
"""
Auto-Fix Script for Structure Violations
Detects and corrects file placement violations with Memory Expert integration
"""

import os
import sys
import json
import yaml
import argparse
import logging
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
import fnmatch

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))
from structure_validator import StructureValidator, Violation

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
STRUCTURE_DIR = PROJECT_ROOT / ".claude" / "structure"
CANONICAL_STRUCTURE_FILE = STRUCTURE_DIR / "canonical-structure.yaml"
MEMORY_EXPERT_FILE = PROJECT_ROOT / ".claude" / "agents" / "memory-expert.md"

class MemoryExpertClient:
    """Mock client for Memory Expert integration"""

    def analyze_file_safety(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze file safety following Memory Expert methodology
        Checks: task board, agent memory, file age, critical patterns
        """
        import glob

        file_name = Path(file_path).name
        file_path_obj = Path(file_path)

        # Initialize safety report
        safety_report = {
            "safe_to_archive": False,
            "active_references": [],
            "last_accessed": datetime.now().isoformat(),
            "lifecycle_status": "unknown",
            "reason": "Unknown"
        }

        # Check 1: AGENT_COMMUNICATION_BOARD.md references
        board_file = PROJECT_ROOT / "AGENT_COMMUNICATION_BOARD.md"
        if board_file.exists():
            board_content = board_file.read_text()
            if file_name in board_content or str(file_path) in board_content:
                safety_report["active_references"].append("AGENT_COMMUNICATION_BOARD.md")
                safety_report["lifecycle_status"] = "active"
                safety_report["reason"] = "Referenced in AGENT_COMMUNICATION_BOARD.md"
                logger.info(f"Memory Expert analysis for {file_name}: {safety_report['safe_to_archive']}")
                logger.info(f"   Reason: {safety_report['reason']}")
                return safety_report

        # Check 2: Agent memory file references
        memory_dir = PROJECT_ROOT / ".claude" / "memory"
        if memory_dir.exists():
            for memory_file in glob.glob(str(memory_dir / "*-memory.json")):
                try:
                    memory_content = Path(memory_file).read_text()
                    if file_name in memory_content or str(file_path) in memory_content:
                        safety_report["active_references"].append(os.path.basename(memory_file))
                        safety_report["lifecycle_status"] = "active"
                        safety_report["reason"] = f"Referenced in {os.path.basename(memory_file)}"
                        logger.info(f"Memory Expert analysis for {file_name}: {safety_report['safe_to_archive']}")
                        logger.info(f"   Reason: {safety_report['reason']}")
                        return safety_report
                except:
                    pass

        # Check 3: Critical system files (never archive)
        critical_patterns = ["MEMORY-EXPERT", "CRITICAL", "SYSTEM", "-memory.json"]
        if any(pattern.lower() in file_name.lower() for pattern in critical_patterns):
            safety_report["lifecycle_status"] = "critical"
            safety_report["reason"] = "Critical system file - never archive"
            logger.info(f"Memory Expert analysis for {file_name}: {safety_report['safe_to_archive']}")
            logger.info(f"   Reason: {safety_report['reason']}")
            return safety_report

        # Check 4: File age + completion status
        try:
            file_stat = file_path_obj.stat()
            age_days = (datetime.now().timestamp() - file_stat.st_mtime) / 86400
            safety_report["last_accessed"] = datetime.fromtimestamp(file_stat.st_mtime).isoformat()

            # Completion reports older than 7 days
            if any(pattern in file_name.upper() for pattern in ["COMPLETE", "COMPLETION"]):
                if age_days > 7:
                    safety_report["safe_to_archive"] = True
                    safety_report["lifecycle_status"] = "completed"
                    safety_report["reason"] = f"Completion report older than 7 days (age: {age_days:.0f} days)"
                    logger.info(f"Memory Expert analysis for {file_name}: {safety_report['safe_to_archive']}")
                    logger.info(f"   Reason: {safety_report['reason']}")
                    return safety_report
        except OSError:
            pass

        # Default: Conservative (keep file)
        safety_report["reason"] = "No archival criteria met - keeping file for safety"
        logger.info(f"Memory Expert analysis for {file_name}: {safety_report['safe_to_archive']}")
        logger.info(f"   Reason: {safety_report['reason']}")
        return safety_report

class AutoFixer:
    """Auto-fix engine for structure violations"""

    def __init__(self, config_file: Optional[Path] = None, dry_run: bool = True):
        self.config_file = config_file or CANONICAL_STRUCTURE_FILE
        self.dry_run = dry_run
        self.config = self._load_config()
        self.validator = StructureValidator(config_file=self.config_file)
        self.memory_expert = MemoryExpertClient()
        self.moves_planned: List[Tuple[Path, Path]] = []
        self.moves_completed: List[Tuple[Path, Path]] = []
        self.unresolved: List[Violation] = []

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration"""
        if not self.config_file.exists():
            logger.error(f"Configuration file not found: {self.config_file}")
            sys.exit(1)

        try:
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML: {e}")
            sys.exit(1)

    def _check_environment(self):
        """Check if running in production environment (safety check)"""
        if os.environ.get('RAILWAY_ENVIRONMENT'):
            logger.error("❌ Auto-fix cannot run on Railway production server!")
            sys.exit(1)

        if os.environ.get('VERCEL'):
            logger.error("❌ Auto-fix cannot run on Vercel deployment!")
            sys.exit(1)

    def _ensure_directory(self, directory: Path):
        """Ensure directory exists"""
        if not directory.exists():
            if self.dry_run:
                logger.info(f"[DRY RUN] Would create directory: {directory}")
            else:
                directory.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {directory}")

    def _validate_path(self, path: Path) -> bool:
        """Validate path for security (prevent path traversal)"""
        try:
            resolved = path.resolve()
            # Python 3.7/3.8 compatibility: emulate is_relative_to
            resolved.relative_to(PROJECT_ROOT)
            return True
        except Exception:
            return False

    def _backup_file(self, file_path: Path):
        """Create backup before moving file"""
        if not self.config.get('settings', {}).get('backup_before_move', True):
            return

        backup_dir = PROJECT_ROOT / ".claude" / "backups" / datetime.now().strftime("%Y%m%d")
        backup_dir.mkdir(parents=True, exist_ok=True)

        backup_path = backup_dir / f"{file_path.name}.{datetime.now().strftime('%H%M%S')}.bak"

        if self.dry_run:
            logger.info(f"[DRY RUN] Would backup: {file_path} → {backup_path}")
        else:
            shutil.copy2(file_path, backup_path)
            logger.info(f"Backed up: {file_path} → {backup_path}")

    def _move_file(self, source: Path, destination: Path) -> bool:
        """Move file to canonical location"""
        # Security check
        if not self._validate_path(source) or not self._validate_path(destination):
            logger.error(f"❌ Invalid path detected - skipping for security")
            return False

        # Check if destination exists
        if destination.exists():
            logger.warning(f"⚠️  Destination already exists: {destination}")
            if self.config.get('settings', {}).get('require_confirmation', True):
                logger.info("Skipping move to avoid overwrite (require_confirmation is enabled)")
                return False

        # Ensure destination directory exists
        self._ensure_directory(destination.parent)

        # Backup if enabled
        self._backup_file(source)

        # Perform move
        if self.dry_run:
            logger.info(f"[DRY RUN] Would move: {source} → {destination}")
            self.moves_planned.append((source, destination))
        else:
            try:
                # Use git mv if in git repository
                result = subprocess.run(
                    ['git', 'mv', str(source), str(destination)],
                    capture_output=True,
                    text=True,
                    cwd=PROJECT_ROOT
                )

                if result.returncode != 0:
                    # Fall back to regular move
                    shutil.move(str(source), str(destination))
                    logger.info(f"Moved (non-git): {source} → {destination}")
                else:
                    logger.info(f"Moved (git): {source} → {destination}")

                self.moves_completed.append((source, destination))
                return True

            except Exception as e:
                logger.error(f"❌ Failed to move {source}: {e}")
                return False

        return True

    def fix_violations(self) -> Tuple[int, int]:
        """Fix all structure violations"""
        # Safety check
        self._check_environment()

        # Get violations
        logger.info("Scanning for structure violations...")
        violations = self.validator.validate_structure()

        if not violations:
            logger.info("✅ No violations found - structure is clean!")
            return 0, 0

        logger.info(f"Found {len(violations)} violations")

        # Group violations by file
        file_violations: Dict[str, Violation] = {}
        for v in violations:
            if v.severity == "error" or (v.severity == "warning" and not self.dry_run):
                file_violations[v.file_path] = v

        fixed_count = 0
        skipped_count = 0

        # Process each violation
        for file_path_str, violation in file_violations.items():
            file_path = Path(file_path_str)

            if not file_path.exists():
                logger.warning(f"File no longer exists: {file_path}")
                continue

            # Query Memory Expert if configured
            if self.config.get('settings', {}).get('query_memory_expert', True):
                safety = self.memory_expert.analyze_file_safety(file_path_str)

                if not safety.get('safe_to_archive', False):
                    logger.warning(f"⚠️  Memory Expert says keep: {file_path.name}")
                    logger.info(f"   Reason: {safety.get('reason', 'Unknown')}")
                    skipped_count += 1
                    continue

            # Determine destination
            if violation.canonical_location and violation.canonical_location != "[should be moved/deleted]":
                destination = PROJECT_ROOT / violation.canonical_location / file_path.name

                if self._move_file(file_path, destination):
                    fixed_count += 1
                else:
                    skipped_count += 1
            else:
                logger.warning(f"⚠️  No canonical location for: {file_path}")
                self.unresolved.append(violation)
                skipped_count += 1

        # Commit changes if configured
        if not self.dry_run and fixed_count > 0:
            self._commit_changes(fixed_count)

        return fixed_count, skipped_count

    def _commit_changes(self, count: int):
        """Commit moved files to git"""
        if not self.config.get('settings', {}).get('git_commit_archives', True):
            return

        try:
            template = self.config.get('settings', {}).get(
                'git_commit_message_template',
                'chore: auto-archive {count} files via structure enforcement'
            )
            message = template.format(count=count)

            # Stage all changes
            subprocess.run(['git', 'add', '.'], cwd=PROJECT_ROOT)

            # Commit
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT
            )

            if result.returncode == 0:
                logger.info(f"✅ Committed {count} file moves")
            else:
                logger.warning(f"Failed to commit: {result.stderr}")

        except Exception as e:
            logger.warning(f"Failed to commit changes: {e}")

    def fix_migration(self) -> Tuple[int, int]:
        """Fix specific migration rules from config"""
        migration_config = self.config.get('migration', {})

        if not migration_config.get('enabled', False):
            logger.info("Migration is disabled in config")
            return 0, 0

        files_to_move = migration_config.get('files_to_move', [])
        fixed_count = 0
        skipped_count = 0

        for move_rule in files_to_move:
            from_pattern = move_rule['from']
            to_location = move_rule['to']

            # Handle glob patterns
            if '*' in from_pattern:
                # Find matching files
                base_path = PROJECT_ROOT / from_pattern.replace('*', '').lstrip('/')
                if base_path.parent.exists():
                    for file_path in base_path.parent.glob(Path(from_pattern).name):
                        destination = PROJECT_ROOT / to_location / file_path.name
                        if self._move_file(file_path, destination):
                            fixed_count += 1
                        else:
                            skipped_count += 1
            else:
                # Direct file path
                source = PROJECT_ROOT / from_pattern.lstrip('/')
                if source.exists():
                    destination = PROJECT_ROOT / to_location / source.name
                    if self._move_file(source, destination):
                        fixed_count += 1
                    else:
                        skipped_count += 1

        return fixed_count, skipped_count

    def print_summary(self, fixed: int, skipped: int):
        """Print operation summary"""
        print("\n" + "="*60)
        print("STRUCTURE AUTO-FIX SUMMARY")
        print("="*60)

        if self.dry_run:
            print("\n🔍 DRY RUN MODE - No actual changes made")
            print(f"\n📋 Would fix: {fixed} violations")
            print(f"📋 Would skip: {skipped} files")

            if self.moves_planned:
                print("\n📁 Planned moves:")
                for source, dest in self.moves_planned[:10]:
                    print(f"  {source.name} → {dest.parent.relative_to(PROJECT_ROOT)}/")
                if len(self.moves_planned) > 10:
                    print(f"  ... and {len(self.moves_planned) - 10} more")

            print("\n💡 To apply these changes, run:")
            print("   python .claude/scripts/auto-fix.py --apply")

        else:
            print(f"\n✅ Fixed: {fixed} violations")
            print(f"⚠️  Skipped: {skipped} files")

            if self.moves_completed:
                print("\n📁 Completed moves:")
                for source, dest in self.moves_completed[:10]:
                    print(f"  ✅ {source.name} → {dest.parent.relative_to(PROJECT_ROOT)}/")
                if len(self.moves_completed) > 10:
                    print(f"  ... and {len(self.moves_completed) - 10} more")

            if self.unresolved:
                print("\n⚠️  Unresolved (no canonical rule):")
                for v in self.unresolved[:10]:
                    print(f"  - {Path(v.file_path).name} (current: {v.current_location})")
                if len(self.unresolved) > 10:
                    print(f"  ... and {len(self.unresolved) - 10} more")

                print("\nNext steps:")
                print("  • Add canonical rules in .claude/structure/canonical-structure.yaml for the above files, or")
                print("  • Move them manually to an allowed archive location.")

        print("\n" + "="*60)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Auto-fix structure violations")
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Preview changes without applying (default)')
    parser.add_argument('--apply', action='store_true',
                       help='Apply fixes (disables dry-run)')
    parser.add_argument('--config', type=Path, help='Custom config file')
    parser.add_argument('--migration', action='store_true',
                       help='Run migration rules from config')
    parser.add_argument('--no-memory-expert', action='store_true',
                       help='Skip Memory Expert queries')
    parser.add_argument('--verbose', action='store_true',
                       help='Verbose output')

    args = parser.parse_args()

    # Set dry_run based on --apply flag
    dry_run = not args.apply

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialize auto-fixer
    fixer = AutoFixer(config_file=args.config, dry_run=dry_run)

    # Disable Memory Expert if requested
    if args.no_memory_expert:
        fixer.config['settings']['query_memory_expert'] = False

    # Run appropriate fix operation
    if args.migration:
        fixed, skipped = fixer.fix_migration()
    else:
        fixed, skipped = fixer.fix_violations()

    # Print summary
    fixer.print_summary(fixed, skipped)

    # Exit code
    sys.exit(0 if fixed > 0 or skipped == 0 else 1)

if __name__ == "__main__":
    main()

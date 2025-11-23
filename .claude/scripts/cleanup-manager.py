#!/usr/bin/env python3
"""
Documentation Manager Automation Script
Orchestrates nightly cleanup with Memory Expert integration
"""

import os
import sys
import json
import yaml
import argparse
import logging
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import fnmatch
import time

# Resolve project root early for logging paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
LOG_PATH = PROJECT_ROOT / ".claude" / "memory" / "cleanup-logs" / "cleanup-manager.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))
from auto_fix import MemoryExpertClient, AutoFixer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('DocumentationManager')

STRUCTURE_DIR = PROJECT_ROOT / ".claude" / "structure"
CANONICAL_STRUCTURE_FILE = STRUCTURE_DIR / "canonical-structure.yaml"
AGENT_BOARD_FILE = PROJECT_ROOT / "AGENT_COMMUNICATION_BOARD.md"
CLEANUP_LOG_DIR = PROJECT_ROOT / ".claude" / "memory" / "cleanup-logs"

class DocumentationManager:
    """Documentation Manager agent implementation"""

    def __init__(self, preview: bool = True):
        self.preview = preview
        self.config = self._load_config()
        self.memory_expert = MemoryExpertClient()
        self.auto_fixer = AutoFixer(dry_run=preview)
        self.cleanup_log = []
        self.start_time = datetime.now()

    def _load_config(self) -> Dict[str, Any]:
        """Load canonical structure configuration"""
        if not CANONICAL_STRUCTURE_FILE.exists():
            logger.error(f"Configuration file not found: {CANONICAL_STRUCTURE_FILE}")
            sys.exit(1)

        try:
            with open(CANONICAL_STRUCTURE_FILE, 'r') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML: {e}")
            sys.exit(1)

    def _check_environment(self):
        """Check if running in production environment (safety check)"""
        if os.environ.get('RAILWAY_ENVIRONMENT'):
            logger.error("❌ Documentation Manager cannot run on Railway production server!")
            sys.exit(1)

        if os.environ.get('VERCEL'):
            logger.error("❌ Documentation Manager cannot run on Vercel deployment!")
            sys.exit(1)

        logger.info("✅ Environment check passed - running locally")

    def _check_lock_file(self) -> bool:
        """Check for lock file to prevent concurrent runs"""
        lock_file = PROJECT_ROOT / ".claude" / "scripts" / ".cleanup.lock"

        if lock_file.exists():
            # Check if lock is stale (older than 1 hour)
            try:
                lock_age = datetime.now() - datetime.fromtimestamp(lock_file.stat().st_mtime)
                if lock_age > timedelta(hours=1):
                    logger.warning("Removing stale lock file")
                    lock_file.unlink()
                else:
                    logger.error("Another cleanup process is running (lock file exists)")
                    return False
            except:
                pass

        # Create lock file
        if not self.preview:
            lock_file.touch()

        return True

    def _remove_lock_file(self):
        """Remove lock file after completion"""
        lock_file = PROJECT_ROOT / ".claude" / "scripts" / ".cleanup.lock"
        if lock_file.exists() and not self.preview:
            lock_file.unlink()

    def _identify_cleanup_candidates(self) -> List[Dict[str, Any]]:
        """Identify files that need cleanup based on lifecycle rules"""
        candidates = []

        for file_type in self.config.get('file_types', []):
            lifecycle = file_type.get('lifecycle_rule', {})
            trigger = lifecycle.get('trigger', 'never')

            if trigger == 'never':
                continue

            # Parse trigger conditions
            patterns = file_type.get('patterns', [])
            canonical_location = file_type.get('canonical_location')

            # Find matching files
            for pattern in patterns:
                for file_path in PROJECT_ROOT.rglob(pattern):
                    if self._evaluate_trigger(file_path, trigger, lifecycle):
                        candidates.append({
                            'file_path': file_path,
                            'file_type': file_type['name'],
                            'action': lifecycle.get('action', 'keep'),
                            'archive_location': lifecycle.get('archive_location'),
                            'query_memory_expert': lifecycle.get('query_memory_expert', True),
                            'reason': self._get_trigger_reason(trigger)
                        })

        return candidates

    def _evaluate_trigger(self, file_path: Path, trigger: str, lifecycle: Dict) -> bool:
        """Evaluate if trigger condition is met"""
        if trigger == 'immediate':
            return True

        # Parse age-based triggers
        if 'file_age >' in trigger:
            try:
                days = int(trigger.split('>')[1].split('days')[0].strip())
                file_age = (datetime.now() - datetime.fromtimestamp(file_path.stat().st_mtime))
                if file_age > timedelta(days=days):
                    # Check additional conditions
                    if 'AND' in trigger:
                        # For now, assume additional conditions are met
                        # In production, would parse and evaluate properly
                        return True
                    return True
            except:
                pass

        return False

    def _get_trigger_reason(self, trigger: str) -> str:
        """Get human-readable trigger reason"""
        if 'file_age' in trigger:
            return f"File age exceeds threshold ({trigger})"
        elif trigger == 'immediate':
            return "Immediate cleanup required"
        else:
            return f"Trigger condition met: {trigger}"

    def _process_candidate(self, candidate: Dict[str, Any]) -> bool:
        """Process a single cleanup candidate"""
        file_path = candidate['file_path']
        action = candidate['action']

        logger.info(f"Processing: {file_path.name}")
        logger.info(f"  Action: {action}")
        logger.info(f"  Reason: {candidate['reason']}")

        # Query Memory Expert if required
        if candidate['query_memory_expert']:
            safety = self.memory_expert.analyze_file_safety(str(file_path))

            if not safety.get('safe_to_archive', False):
                logger.warning(f"  ⚠️  Memory Expert says KEEP: {safety.get('reason')}")
                self.cleanup_log.append({
                    'file': str(file_path),
                    'action': 'skipped',
                    'reason': f"Memory Expert: {safety.get('reason')}"
                })
                return False

        # Perform action
        if action == 'archive':
            return self._archive_file(file_path, candidate.get('archive_location'))
        elif action == 'delete':
            return self._delete_file(file_path)
        else:
            logger.info(f"  ℹ️  Action '{action}' - no operation needed")
            return True

    def _archive_file(self, file_path: Path, archive_location: Optional[str]) -> bool:
        """Archive a file to specified location"""
        if not archive_location:
            # Use default archive location
            archive_location = ".claude/archive/"

        destination = PROJECT_ROOT / archive_location / file_path.name

        if self.preview:
            logger.info(f"  [PREVIEW] Would archive to: {destination}")
            self.cleanup_log.append({
                'file': str(file_path),
                'action': 'would_archive',
                'destination': str(destination)
            })
            return True

        try:
            # Ensure destination directory exists
            destination.parent.mkdir(parents=True, exist_ok=True)

            # Use git mv if possible
            result = subprocess.run(
                ['git', 'mv', str(file_path), str(destination)],
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT
            )

            if result.returncode == 0:
                logger.info(f"  ✅ Archived to: {destination}")
                self.cleanup_log.append({
                    'file': str(file_path),
                    'action': 'archived',
                    'destination': str(destination)
                })
                return True
            else:
                logger.error(f"  ❌ Failed to archive: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"  ❌ Archive failed: {e}")
            return False

    def _delete_file(self, file_path: Path) -> bool:
        """Delete a file (only for temporary files)"""
        # Safety: Only delete specific temporary patterns
        safe_patterns = ['*.tmp', '*.temp', '*~', '.*.swp', '*.bak']

        if not any(fnmatch.fnmatch(file_path.name, pattern) for pattern in safe_patterns):
            logger.warning(f"  ⚠️  Refusing to delete non-temporary file: {file_path.name}")
            return False

        if self.preview:
            logger.info(f"  [PREVIEW] Would delete: {file_path}")
            self.cleanup_log.append({
                'file': str(file_path),
                'action': 'would_delete'
            })
            return True

        try:
            file_path.unlink()
            logger.info(f"  ✅ Deleted: {file_path}")
            self.cleanup_log.append({
                'file': str(file_path),
                'action': 'deleted'
            })
            return True
        except Exception as e:
            logger.error(f"  ❌ Delete failed: {e}")
            return False

    def _update_communication_board(self):
        """Update AGENT_COMMUNICATION_BOARD.md with cleanup results"""
        if not AGENT_BOARD_FILE.exists():
            logger.warning("Communication board not found")
            return

        if self.preview:
            logger.info("[PREVIEW] Would update AGENT_COMMUNICATION_BOARD.md")
            return

        try:
            # Read current content
            with open(AGENT_BOARD_FILE, 'r') as f:
                content = f.read()

            # Add cleanup entry
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            entry = f"\n- **[CLEANUP]** Documentation Manager cleanup – @documentation-manager ✅ ({timestamp} - {len(self.cleanup_log)} files processed)"

            # Find appropriate section and add entry
            if "## ✅ Completed Today" in content:
                content = content.replace(
                    "## ✅ Completed Today",
                    f"## ✅ Completed Today\n{entry}"
                )
            else:
                content += f"\n{entry}"

            # Write updated content
            with open(AGENT_BOARD_FILE, 'w') as f:
                f.write(content)

            logger.info("✅ Updated AGENT_COMMUNICATION_BOARD.md")

        except Exception as e:
            logger.error(f"Failed to update communication board: {e}")

    def _save_cleanup_log(self):
        """Save cleanup log to file"""
        CLEANUP_LOG_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = CLEANUP_LOG_DIR / f"cleanup_{timestamp}.json"

        log_data = {
            'timestamp': datetime.now().isoformat(),
            'preview_mode': self.preview,
            'duration_seconds': (datetime.now() - self.start_time).total_seconds(),
            'files_processed': len(self.cleanup_log),
            'actions': self.cleanup_log
        }

        try:
            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2, default=str)

            logger.info(f"✅ Cleanup log saved: {log_file}")
        except Exception as e:
            logger.error(f"Failed to save cleanup log: {e}")

    def _commit_changes(self):
        """Commit cleanup changes to git"""
        if self.preview:
            logger.info("[PREVIEW] Would commit changes to git")
            return

        if not self.cleanup_log:
            logger.info("No changes to commit")
            return

        try:
            # Stage all changes
            subprocess.run(['git', 'add', '.'], cwd=PROJECT_ROOT)

            # Commit
            message = f"chore: Documentation Manager cleanup - {len(self.cleanup_log)} files processed"
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT
            )

            if result.returncode == 0:
                logger.info(f"✅ Committed cleanup changes")
            else:
                logger.warning(f"Git commit failed: {result.stderr}")

        except Exception as e:
            logger.warning(f"Failed to commit changes: {e}")

    def run_cleanup(self):
        """Main cleanup orchestration"""
        logger.info("="*60)
        logger.info("DOCUMENTATION MANAGER CLEANUP")
        logger.info("="*60)
        logger.info(f"Start time: {self.start_time}")
        logger.info(f"Mode: {'PREVIEW' if self.preview else 'APPLY'}")

        # Safety checks
        self._check_environment()

        if not self._check_lock_file():
            sys.exit(1)

        try:
            # Step 1: Run structure auto-fix
            logger.info("\n📋 Step 1: Running structure auto-fix...")
            fixed, skipped = self.auto_fixer.fix_violations()
            logger.info(f"  Structure fixes: {fixed} fixed, {skipped} skipped")

            # Step 2: Identify cleanup candidates
            logger.info("\n📋 Step 2: Identifying cleanup candidates...")
            candidates = self._identify_cleanup_candidates()
            logger.info(f"  Found {len(candidates)} cleanup candidates")

            # Step 3: Process each candidate
            if candidates:
                logger.info("\n📋 Step 3: Processing candidates...")
                for candidate in candidates:
                    self._process_candidate(candidate)

            # Step 4: Update communication board
            logger.info("\n📋 Step 4: Updating communication board...")
            self._update_communication_board()

            # Step 5: Save cleanup log
            logger.info("\n📋 Step 5: Saving cleanup log...")
            self._save_cleanup_log()

            # Step 6: Commit changes
            if not self.preview:
                logger.info("\n📋 Step 6: Committing changes...")
                self._commit_changes()

            # Summary
            duration = (datetime.now() - self.start_time).total_seconds()
            logger.info("\n" + "="*60)
            logger.info("CLEANUP COMPLETE")
            logger.info(f"Duration: {duration:.1f} seconds")
            logger.info(f"Files processed: {len(self.cleanup_log)}")

            if self.preview:
                logger.info("\n💡 This was a PREVIEW run. To apply changes:")
                logger.info("   python .claude/scripts/cleanup-manager.py --apply")

        finally:
            self._remove_lock_file()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Documentation Manager cleanup orchestration")
    parser.add_argument('--preview', action='store_true', default=True,
                       help='Preview mode - show what would be done (default)')
    parser.add_argument('--apply', action='store_true',
                       help='Apply changes (disables preview mode)')
    parser.add_argument('--verbose', action='store_true',
                       help='Verbose output')

    args = parser.parse_args()

    # Set preview based on --apply flag
    preview = not args.apply

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialize and run
    manager = DocumentationManager(preview=preview)
    manager.run_cleanup()

if __name__ == "__main__":
    main()

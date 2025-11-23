#!/usr/bin/env python3
"""
Claude Code Project Template - Interactive Setup Wizard
Bootstraps a new project with agents, structure enforcement, and memory system
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

try:
    import yaml
    from jinja2 import Template
    import questionary
except ImportError:
    print("❌ Missing required dependencies!")
    print("\nPlease install:")
    print("  pip install PyYAML jinja2 questionary")
    sys.exit(1)

# Colors
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text: str):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text: str):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

class SetupWizard:
    def __init__(self):
        self.template_root = Path(__file__).parent.resolve()
        self.project_root = Path.cwd()
        self.config = {}

    def run(self):
        """Main setup flow"""
        print_header("Claude Code Project Setup Wizard")

        print("🚀 Welcome! This wizard will set up your project with:")
        print("   • 15 specialized AI agents")
        print("   • Automated structure enforcement")
        print("   • Tri-tier memory system")
        print("   • Quality gates & reflection")
        print()

        # Check prerequisites
        if not self.check_prerequisites():
            return False

        # Gather project information
        if not self.gather_project_info():
            return False

        # Choose tier
        if not self.choose_tier():
            return False

        # Copy template files based on tier
        if not self.copy_template_files():
            return False

        # Render Jinja2 templates
        if not self.render_templates():
            return False

        # Install git hooks
        if not self.install_git_hooks():
            return False

        # Initialize memory system
        if not self.initialize_memory():
            return False

        # Run validation
        if not self.validate_setup():
            return False

        # Show success message
        self.show_success_message()

        return True

    def check_prerequisites(self) -> bool:
        """Check Python version, git, etc."""
        print_header("Checking Prerequisites")

        # Check Python version
        if sys.version_info < (3, 8):
            print_error("Python 3.8+ required")
            print(f"Current version: {sys.version_info.major}.{sys.version_info.minor}")
            return False
        print_success(f"Python {sys.version_info.major}.{sys.version_info.minor} found")

        # Check if git is installed
        if not shutil.which('git'):
            print_error("Git not found - please install git")
            return False
        print_success("Git found")

        # Check if in git repository
        try:
            subprocess.run(['git', 'rev-parse', '--git-dir'],
                          check=True, capture_output=True, cwd=self.project_root)
            print_success("Git repository detected")
        except subprocess.CalledProcessError:
            print_warning("Not in a git repository")
            init_git = questionary.confirm("Initialize git repository?").ask()
            if init_git:
                subprocess.run(['git', 'init'], cwd=self.project_root, check=True)
                print_success("Git repository initialized")
            else:
                print_warning("Proceeding without git (hooks will not work)")

        return True

    def gather_project_info(self) -> bool:
        """Gather project details from user"""
        print_header("Project Information")

        # Project name
        default_name = self.project_root.name
        self.config['project_name'] = questionary.text(
            "Project name?",
            default=default_name
        ).ask()

        # Project slug (for URLs)
        default_slug = self.config['project_name'].lower().replace(' ', '-')
        self.config['project_slug'] = questionary.text(
            "Project slug (for URLs)?",
            default=default_slug
        ).ask()

        # Description
        self.config['project_description'] = questionary.text(
            "Brief description?",
            default="A production-ready application"
        ).ask()

        # Admin email
        self.config['admin_email'] = questionary.text(
            "Admin email?",
            default="admin@example.com"
        ).ask()

        # Frontend framework
        self.config['frontend_framework'] = questionary.select(
            "Frontend framework?",
            choices=["React", "Vue", "Angular", "Svelte", "Next.js", "Nuxt", "Other"]
        ).ask()

        # Frontend language
        self.config['frontend_language'] = questionary.select(
            "Frontend language?",
            choices=["TypeScript", "JavaScript"]
        ).ask()

        # Backend framework
        self.config['backend_framework'] = questionary.select(
            "Backend framework?",
            choices=["FastAPI", "Express", "Django", "Flask", "NestJS", "Go (Gin)", "Other"]
        ).ask()

        # Backend language
        backend_lang_map = {
            "FastAPI": "Python",
            "Django": "Python",
            "Flask": "Python",
            "Express": "Node.js",
            "NestJS": "Node.js",
            "Go (Gin)": "Go"
        }
        self.config['backend_language'] = backend_lang_map.get(
            self.config['backend_framework'],
            "Python"
        )

        # Frontend platform
        self.config['frontend_platform'] = questionary.select(
            "Frontend deployment platform?",
            choices=["Vercel", "Netlify", "Cloudflare Pages", "AWS", "GCP", "Other"]
        ).ask()

        # Backend platform
        self.config['backend_platform'] = questionary.select(
            "Backend deployment platform?",
            choices=["Railway", "Render", "AWS", "GCP", "Heroku", "DigitalOcean", "Other"]
        ).ask()

        # URLs (optional)
        self.config['frontend_prod_url'] = f"https://{self.config['project_slug']}.vercel.app"
        self.config['frontend_staging_url'] = f"https://{self.config['project_slug']}-staging.vercel.app"
        self.config['backend_prod_url'] = f"https://{self.config['project_slug']}-production.up.railway.app"
        self.config['backend_staging_url'] = f"https://{self.config['project_slug']}-staging.up.railway.app"

        # CI/CD
        self.config['ci_cd_platform'] = "GitHub Actions"
        self.config['monitoring_platform'] = "None"

        # Timestamps
        self.config['setup_date'] = datetime.now().isoformat()
        self.config['current_date'] = datetime.now().strftime("%Y-%m-%d")

        # Project root
        self.config['project_root'] = str(self.project_root)

        return True

    def choose_tier(self) -> bool:
        """Let user choose tier (minimal, standard, complete)"""
        print_header("Choose Your Tier")

        print("📊 Tier Comparison:\n")
        print("1. MINIMAL (30-minute setup)")
        print("   • 5 core agents (Atharva, Anand, Ankur, Debugger, Memory)")
        print("   • Basic structure validation")
        print("   • Pre-commit hook only")
        print("   → Good for: Prototypes, learning, small projects\n")

        print("2. STANDARD (2-hour setup) ⭐ RECOMMENDED")
        print("   • All 15 agents")
        print("   • Full structure enforcement + auto-fix")
        print("   • Tri-tier memory system")
        print("   • All 3 git hooks")
        print("   • Documentation architecture")
        print("   → Good for: Production projects, teams\n")

        print("3. COMPLETE (1-day setup)")
        print("   • Everything in Standard +")
        print("   • Silent reflection system")
        print("   • Automated cleanup (cron)")
        print("   • Advanced monitoring")
        print("   → Good for: Large projects, mission-critical\n")

        tier = questionary.select(
            "Which tier?",
            choices=[
                "Minimal (30 min, 5 agents, basic structure)",
                "Standard (2 hours, 15 agents, full system) ⭐",
                "Complete (1 day, everything + automation)"
            ],
            default="Standard (2 hours, 15 agents, full system) ⭐"
        ).ask()

        if "Minimal" in tier:
            self.config['tier'] = "minimal"
            self.config['enable_structure_enforcement'] = True
            self.config['enable_memory_system'] = False
            self.config['enable_reflection_system'] = False
            self.config['enable_automated_cleanup'] = False
        elif "Standard" in tier:
            self.config['tier'] = "standard"
            self.config['enable_structure_enforcement'] = True
            self.config['enable_memory_system'] = True
            self.config['enable_reflection_system'] = False
            self.config['enable_automated_cleanup'] = False
        else:  # Complete
            self.config['tier'] = "complete"
            self.config['enable_structure_enforcement'] = True
            self.config['enable_memory_system'] = True
            self.config['enable_reflection_system'] = True
            self.config['enable_automated_cleanup'] = True

        print_success(f"Selected: {self.config['tier'].upper()} tier")
        return True

    def copy_template_files(self) -> bool:
        """Copy template files to project directory"""
        print_header("Copying Template Files")

        # Copy .claude directory structure
        for subdir in ['agents', 'docs', 'hooks', 'memory', 'scripts', 'structure', 'config']:
            src = self.template_root / '.claude' / subdir
            dst = self.project_root / '.claude' / subdir

            if src.exists():
                if dst.exists():
                    print_warning(f"Directory exists: .claude/{subdir} (skipping)")
                else:
                    shutil.copytree(src, dst)
                    print_success(f"Copied .claude/{subdir}")

        # Copy documentation
        docs_src = self.template_root / 'docs'
        docs_dst = self.project_root / 'docs'
        if docs_src.exists() and not docs_dst.exists():
            shutil.copytree(docs_src, docs_dst)
            print_success("Copied documentation")

        # Copy tests
        tests_src = self.template_root / 'tests'
        tests_dst = self.project_root / 'tests'
        if tests_src.exists() and not tests_dst.exists():
            shutil.copytree(tests_src, tests_dst)
            print_success("Copied validation tests")

        return True

    def render_templates(self) -> bool:
        """Render all Jinja2 templates"""
        print_header("Generating Configuration Files")

        templates = [
            (self.template_root / 'CLAUDE.md.j2',
             self.project_root / 'CLAUDE.md'),
            (self.template_root / 'AGENT_COMMUNICATION_BOARD.md.j2',
             self.project_root / 'AGENT_COMMUNICATION_BOARD.md'),
            (self.project_root / '.claude/config/project-config.yaml.j2',
             self.project_root / '.claude/config/project-config.yaml'),
            (self.project_root / '.claude/config/reflection-config.json.j2',
             self.project_root / '.claude/config/reflection-config.json'),
        ]

        for template_path, output_path in templates:
            if template_path.exists():
                with open(template_path, 'r') as f:
                    template = Template(f.read())

                rendered = template.render(**self.config)

                with open(output_path, 'w') as f:
                    f.write(rendered)

                print_success(f"Generated {output_path.name}")
            else:
                print_warning(f"Template not found: {template_path.name}")

        return True

    def install_git_hooks(self) -> bool:
        """Install git hooks"""
        print_header("Installing Git Hooks")

        install_script = self.project_root / '.claude/scripts/install-hooks.sh'
        if install_script.exists():
            try:
                result = subprocess.run(
                    ['bash', str(install_script)],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print_success("Git hooks installed")
                    return True
                else:
                    print_error(f"Hook installation failed: {result.stderr}")
                    return False
            except Exception as e:
                print_error(f"Failed to install hooks: {e}")
                return False
        else:
            print_warning("install-hooks.sh not found (skipping hooks)")
            return True

    def initialize_memory(self) -> bool:
        """Initialize memory files for agents"""
        print_header("Initializing Memory System")

        if not self.config.get('enable_memory_system'):
            print_warning("Memory system disabled in this tier")
            return True

        # List of agents to create memory for
        agents = [
            "anand-2.0", "atharva-2.0", "ankur-2.0", "sama-2.0", "shawar-2.0",
            "hitesh-2.0", "harshit-2.0", "vidya-2.0", "varsha-2.0",
            "debugger", "bug-fix-orchestrator", "memory-expert",
            "reflection-expert", "documentation-manager"
        ]

        template_file = self.project_root / '.claude/memory/agent-memory-template.json'
        if not template_file.exists():
            print_warning("Memory template not found (skipping memory init)")
            return True

        with open(template_file, 'r') as f:
            template_data = json.load(f)

        for agent in agents:
            memory_file = self.project_root / f'.claude/memory/{agent}-memory.json'
            if not memory_file.exists():
                memory_data = template_data.copy()
                memory_data['agent_name'] = agent
                memory_data['last_updated'] = datetime.now().isoformat()

                # Remove template comments
                if '_comment' in memory_data:
                    del memory_data['_comment']
                if '_instructions' in memory_data:
                    del memory_data['_instructions']

                # Clean sub-sections
                for section in ['hot_memory', 'warm_memory', 'cold_memory']:
                    if section in memory_data and '_description' in memory_data[section]:
                        del memory_data[section]['_description']

                with open(memory_file, 'w') as f:
                    json.dump(memory_data, f, indent=2)

                print_success(f"Initialized memory for {agent}")

        return True

    def validate_setup(self) -> bool:
        """Run validation tests"""
        print_header("Validating Setup")

        validate_script = self.project_root / 'tests/validate_setup.py'
        if validate_script.exists():
            try:
                result = subprocess.run(
                    ['python3', str(validate_script)],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True
                )
                print(result.stdout)
                if result.returncode == 0:
                    print_success("All validation checks passed!")
                    return True
                else:
                    print_warning("Some validation checks failed (see above)")
                    return True  # Non-fatal
            except Exception as e:
                print_warning(f"Validation script failed: {e}")
                return True  # Non-fatal
        else:
            print_warning("Validation script not found (skipping validation)")
            return True

    def show_success_message(self):
        """Show final success message"""
        print_header("Setup Complete!")

        print(f"{Colors.GREEN}🎉 Your project is ready!{Colors.END}\n")

        print(f"{Colors.BOLD}Project:{Colors.END} {self.config['project_name']}")
        print(f"{Colors.BOLD}Tier:{Colors.END} {self.config['tier'].upper()}")
        print(f"{Colors.BOLD}Agents:{Colors.END} {'15' if self.config['tier'] != 'minimal' else '5'} specialized agents")
        print()

        print(f"{Colors.BOLD}Next Steps:{Colors.END}")
        print("1. Read the quick start guide:")
        print(f"   docs/QUICK_START_{self.config['tier'].upper()}.md")
        print()
        print("2. Invoke your first agent:")
        print("   @anand-2.0 help me get started")
        print()
        print("3. Make a test commit to verify git hooks:")
        print("   git add CLAUDE.md")
        print("   git commit -m '[SETUP-001] Initial project setup'")
        print()

        print(f"{Colors.YELLOW}⚡ Pro tip:{Colors.END} Check AGENT_COMMUNICATION_BOARD.md to track progress")
        print()

def main():
    wizard = SetupWizard()
    success = wizard.run()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

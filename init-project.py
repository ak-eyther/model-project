#!/usr/bin/env python3
"""
Project Initialization Wizard
Customizes the template for a new project by replacing placeholders
"""
import sys
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime

try:
    import questionary
    import yaml
except ImportError:
    print("❌ Missing dependencies. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "questionary", "PyYAML"], check=True)
    import questionary
    import yaml

# Color formatting
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.YELLOW}ℹ️  {text}{Colors.END}")

def get_project_info():
    """Collect project information from user"""
    print_header("🚀 New Project Setup Wizard")

    print_info("This wizard will customize the template for your new project.\n")

    # Project basics
    project_name = questionary.text(
        "Project name (e.g., 'Task Manager Pro', 'E-commerce Dashboard'):",
        validate=lambda x: len(x) > 0
    ).ask()

    project_slug = questionary.text(
        "Project slug (for URLs, e.g., 'task-manager-pro'):",
        default=project_name.lower().replace(' ', '-')
    ).ask()

    project_description = questionary.text(
        "Short description:",
        default=f"{project_name} - Built with Next.js + FastAPI"
    ).ask()

    # Tech stack
    print_info("\n📚 Tech Stack Configuration")

    frontend_framework = questionary.select(
        "Frontend framework:",
        choices=["Next.js", "React (Vite)", "Vue.js"]
    ).ask()

    backend_framework = questionary.select(
        "Backend framework:",
        choices=["FastAPI", "Express.js", "Django", "Flask"]
    ).ask()

    use_ai = questionary.confirm(
        "Will this project use AI/ML features?",
        default=False
    ).ask()

    # Deployment
    print_info("\n🚀 Deployment Configuration")

    frontend_platform = questionary.select(
        "Frontend deployment platform:",
        choices=["Vercel", "Netlify", "AWS Amplify", "Other"]
    ).ask()

    backend_platform = questionary.select(
        "Backend deployment platform:",
        choices=["Railway", "Render", "AWS", "Google Cloud", "Other"]
    ).ask()

    # Domain context
    print_info("\n🏢 Project Context")

    domain = questionary.select(
        "Domain/Industry:",
        choices=[
            "Healthcare", "Finance", "E-commerce", "Education",
            "SaaS", "Internal Tools", "Other"
        ]
    ).ask()

    # Author info
    print_info("\n👤 Author Information")

    author_name = questionary.text(
        "Your name:",
        default="Arif Khan"
    ).ask()

    author_email = questionary.text(
        "Your email:",
        default="arif.khan@vitraya.com"
    ).ask()

    github_repo = questionary.text(
        "GitHub repository URL (optional):",
        default=""
    ).ask()

    return {
        "project": {
            "name": project_name,
            "slug": project_slug,
            "description": project_description,
            "created": datetime.now().isoformat(),
            "author": {
                "name": author_name,
                "email": author_email
            },
            "repository": github_repo or f"https://github.com/{author_name.lower().replace(' ', '')}/{project_slug}"
        },
        "tech_stack": {
            "frontend": {
                "framework": frontend_framework,
                "language": "TypeScript"
            },
            "backend": {
                "framework": backend_framework,
                "language": "Python" if backend_framework in ["FastAPI", "Django", "Flask"] else "TypeScript"
            },
            "ai_ml": {
                "enabled": use_ai,
                "provider": "Claude (Anthropic)" if use_ai else None
            }
        },
        "deployment": {
            "frontend": {
                "platform": frontend_platform,
                "url": {
                    "production": f"https://{project_slug}.{frontend_platform.lower()}.app",
                    "staging": f"https://{project_slug}-staging.{frontend_platform.lower()}.app"
                }
            },
            "backend": {
                "platform": backend_platform,
                "url": {
                    "production": f"https://{project_slug}-production.up.{backend_platform.lower()}.app",
                    "staging": f"https://{project_slug}-staging.up.{backend_platform.lower()}.app"
                }
            }
        },
        "domain": {
            "industry": domain,
            "context": f"{domain} application built with {frontend_framework} and {backend_framework}"
        }
    }

def update_package_json(project_info):
    """Update package.json with project details"""
    package_json_path = Path("package.json")

    if not package_json_path.exists():
        print_error("package.json not found")
        return

    with open(package_json_path, 'r') as f:
        package_data = json.load(f)

    # Update package.json fields
    package_data["name"] = project_info["project"]["slug"]
    package_data["description"] = project_info["project"]["description"]
    package_data["version"] = "0.1.0"
    package_data["author"] = f"{project_info['project']['author']['name']} <{project_info['project']['author']['email']}>"

    if project_info["project"]["repository"]:
        package_data["repository"] = {
            "type": "git",
            "url": project_info["project"]["repository"]
        }

    with open(package_json_path, 'w') as f:
        json.dump(package_data, f, indent=2)

    print_success(f"Updated package.json → {project_info['project']['slug']}")

def update_layout_tsx(project_info):
    """Update app/layout.tsx with project name"""
    layout_path = Path("app/layout.tsx")

    if not layout_path.exists():
        return

    content = layout_path.read_text()

    # Replace title and description
    content = re.sub(
        r"title: '[^']*'",
        f"title: '{project_info['project']['name']}'",
        content
    )
    content = re.sub(
        r"description: '[^']*'",
        f"description: '{project_info['project']['description']}'",
        content
    )

    layout_path.write_text(content)
    print_success(f"Updated app/layout.tsx → {project_info['project']['name']}")

def update_home_page(project_info):
    """Update app/page.tsx with project name"""
    page_path = Path("app/page.tsx")

    if not page_path.exists():
        return

    content = page_path.read_text()

    # Replace project name
    content = content.replace(
        "Claude Code Project Template",
        project_info['project']['name']
    )

    page_path.write_text(content)
    print_success(f"Updated app/page.tsx → {project_info['project']['name']}")

def update_fastapi_main(project_info):
    """Update main.py with project details"""
    main_path = Path("main.py")

    if not main_path.exists():
        return

    content = main_path.read_text()

    # Replace title and description
    content = re.sub(
        r'title="[^"]*"',
        f'title="{project_info["project"]["name"]} API"',
        content
    )
    content = re.sub(
        r'description="[^"]*"',
        f'description="{project_info["project"]["description"]}"',
        content
    )
    content = content.replace(
        'FastAPI Backend for Claude Code Project Template',
        f'FastAPI Backend for {project_info["project"]["name"]}'
    )
    content = content.replace(
        '"message": "Claude Code Project Template API"',
        f'"message": "{project_info["project"]["name"]} API"'
    )

    main_path.write_text(content)
    print_success(f"Updated main.py → {project_info['project']['name']} API")

def create_project_context(project_info):
    """Create .claude/context/project-context.yaml"""
    context_dir = Path(".claude/context")
    context_dir.mkdir(parents=True, exist_ok=True)

    context_path = context_dir / "project-context.yaml"

    with open(context_path, 'w') as f:
        yaml.dump(project_info, f, default_flow_style=False, sort_keys=False)

    print_success(f"Created .claude/context/project-context.yaml")

def update_readme(project_info):
    """Update README.md with project name"""
    readme_path = Path("README.md")

    if not readme_path.exists():
        return

    content = readme_path.read_text()

    # Replace project name in title
    content = re.sub(
        r"# Claude Code Project Template",
        f"# {project_info['project']['name']}",
        content,
        count=1
    )

    # Update description
    content = re.sub(
        r"> \*\*Production-ready agent orchestration infrastructure for any project\*\*",
        f"> **{project_info['project']['description']}**",
        content
    )

    readme_path.write_text(content)
    print_success(f"Updated README.md → {project_info['project']['name']}")

def main():
    """Main wizard flow"""
    try:
        # Check if already initialized
        context_file = Path(".claude/context/project-context.yaml")
        if context_file.exists():
            overwrite = questionary.confirm(
                "⚠️  Project already initialized. Overwrite?",
                default=False
            ).ask()
            if not overwrite:
                print_info("Initialization cancelled.")
                return

        # Collect project info
        project_info = get_project_info()

        # Show summary
        print_header("📋 Project Configuration Summary")
        print(f"Project: {Colors.BOLD}{project_info['project']['name']}{Colors.END}")
        print(f"Slug: {project_info['project']['slug']}")
        print(f"Tech Stack: {project_info['tech_stack']['frontend']['framework']} + {project_info['tech_stack']['backend']['framework']}")
        print(f"Deployment: {project_info['deployment']['frontend']['platform']} + {project_info['deployment']['backend']['platform']}")
        print(f"Domain: {project_info['domain']['industry']}\n")

        confirm = questionary.confirm("Proceed with initialization?", default=True).ask()
        if not confirm:
            print_info("Initialization cancelled.")
            return

        # Apply changes
        print_header("🔧 Customizing Template")

        update_package_json(project_info)
        update_layout_tsx(project_info)
        update_home_page(project_info)
        update_fastapi_main(project_info)
        create_project_context(project_info)
        update_readme(project_info)

        # Success message
        print_header("🎉 Initialization Complete!")
        print_success(f"Your project '{project_info['project']['name']}' is ready!")
        print_info("\n📚 Next Steps:")
        print(f"   1. Run: {Colors.BOLD}./setup.sh{Colors.END} (install dependencies)")
        print(f"   2. Start frontend: {Colors.BOLD}npm run dev{Colors.END}")
        print(f"   3. Start backend: {Colors.BOLD}uvicorn main:app --reload{Colors.END}")
        print(f"   4. Visit: {Colors.BOLD}http://localhost:3000{Colors.END}")
        print(f"\n   All 15 AI agents now know about '{project_info['project']['name']}'! 🚀\n")

    except KeyboardInterrupt:
        print_error("\n\nInitialization cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error during initialization: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

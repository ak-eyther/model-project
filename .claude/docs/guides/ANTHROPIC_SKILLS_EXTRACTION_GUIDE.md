# Anthropic Skills Extraction Guide

**Purpose:** Extract and implement skills from https://github.com/anthropics/skills into this or any other project.

**Last Updated:** 2025-11-23

---

## 📋 Available Skills Catalog

### 🎨 Creative & Design Skills

#### 1. algorithmic-art
- **What it does:** Creates generative art using p5.js with seeded randomness, flow fields, and particle systems
- **Use cases:** Creating unique visual art programmatically, generating backgrounds, artistic visualizations
- **Dependencies:** p5.js library
- **Portability:** ✅ High (JavaScript-based, works in any web project)
- **Implementation complexity:** Medium

#### 2. canvas-design
- **What it does:** Designs beautiful visual art in .png and .pdf formats using design philosophies
- **Use cases:** Creating posters, static designs, marketing materials
- **Dependencies:** PNG/PDF generation libraries
- **Portability:** ✅ High (output-agnostic)
- **Implementation complexity:** Medium

#### 3. slack-gif-creator
- **What it does:** Creates animated GIFs optimized for Slack's size constraints (validators + composable animation primitives)
- **Use cases:** Creating custom Slack emoji, reaction GIFs, team communication assets
- **Dependencies:** GIF animation tools, Slack size specifications
- **Portability:** ✅ High (useful for any team using Slack)
- **Implementation complexity:** Low-Medium

---

### 💻 Development & Technical Skills

#### 4. web-artifacts-builder (artifacts-builder)
- **What it does:** Builds complex claude.ai HTML artifacts using React, Tailwind CSS, and shadcn/ui components
- **Use cases:** Creating interactive web components, multi-component applications with state management
- **Dependencies:** React, Tailwind CSS, shadcn/ui
- **Portability:** ⚠️ Medium (requires React ecosystem)
- **Implementation complexity:** High
- **Note:** Best for complex artifacts requiring routing and state management

#### 5. mcp-builder (mcp-server)
- **What it does:** Guide for creating high-quality MCP (Model Context Protocol) servers for integrating external APIs
- **Use cases:** Building MCP servers to integrate external services, API wrappers for LLMs
- **Dependencies:** FastMCP (Python) or MCP SDK (Node/TypeScript)
- **Portability:** ✅ High (language-agnostic concept)
- **Implementation complexity:** Medium-High
- **Note:** Essential for extending Claude's capabilities with custom tools

#### 6. webapp-testing
- **What it does:** Tests local web applications using Playwright (frontend verification, debugging UI, screenshots, logs)
- **Use cases:** Automated testing, UI debugging, visual regression testing
- **Dependencies:** Playwright
- **Portability:** ✅ High (works with any web application)
- **Implementation complexity:** Low-Medium

---

### 📄 Document Skills (Source-Available)

#### 7. docx
- **What it does:** Comprehensive Word document creation, editing, tracked changes, comments, formatting preservation
- **Use cases:** Generating reports, creating professional documents, document templates
- **Dependencies:** Python docx library
- **Portability:** ✅ High (Python-based)
- **Implementation complexity:** Medium
- **License:** Source-available (not open source)

#### 8. pdf
- **What it does:** PDF manipulation toolkit (extract text/tables, create PDFs, merge/split, fill forms)
- **Use cases:** Document processing, form filling, PDF generation, text extraction
- **Dependencies:** PDF processing library (Python)
- **Portability:** ✅ High (Python-based)
- **Implementation complexity:** Medium
- **License:** Source-available (not open source)

#### 9. pptx
- **What it does:** PowerPoint creation, editing, layouts, comments, speaker notes
- **Use cases:** Generating presentations, automated slide decks, report generation
- **Dependencies:** Python pptx library
- **Portability:** ✅ High (Python-based)
- **Implementation complexity:** Medium
- **License:** Source-available (not open source)

#### 10. xlsx
- **What it does:** Spreadsheet creation, editing, analysis with formulas, formatting, data analysis, visualization
- **Use cases:** Data reporting, automated spreadsheets, data transformation
- **Dependencies:** Python xlsx library
- **Portability:** ✅ High (Python-based)
- **Implementation complexity:** Medium
- **License:** Source-available (not open source)

---

### 📝 Enterprise & Communication Skills

#### 11. brand-guidelines
- **What it does:** Applies Anthropic's official brand colors and typography to artifacts
- **Use cases:** Enforcing brand consistency, creating branded content
- **Dependencies:** Anthropic brand specifications
- **Portability:** ⚠️ Low (Anthropic-specific, but concept is reusable)
- **Implementation complexity:** Low
- **Adaptation:** Replace with your own brand guidelines

#### 12. internal-comms
- **What it does:** Writes internal communications (status reports, newsletters, FAQs, incident reports, project updates)
- **Use cases:** Corporate communications, team updates, documentation
- **Dependencies:** None
- **Portability:** ✅ High (company-agnostic templates)
- **Implementation complexity:** Low
- **Adaptation:** Customize formats to your company's style

#### 13. theme-factory
- **What it does:** Styles artifacts with 10 pre-set themes or generates custom themes on-the-fly (colors, fonts, layouts)
- **Use cases:** Consistent styling across documents, rapid prototyping, design systems
- **Dependencies:** Theme templates, CSS generation
- **Portability:** ✅ High (CSS-based)
- **Implementation complexity:** Medium

---

### 🛠️ Meta Skills (Skill Creation Tools)

#### 14. skill-creator
- **What it does:** Guide for creating effective skills that extend Claude's capabilities
- **Use cases:** Learning how to create custom skills, skill development education
- **Dependencies:** Understanding of SKILL.md format
- **Portability:** ✅ High (educational resource)
- **Implementation complexity:** N/A (documentation)
- **Note:** Essential for creating your own custom skills

#### 15. template-skill
- **What it does:** Basic template to use as a starting point for new skills
- **Use cases:** Boilerplate for new skill creation
- **Dependencies:** None
- **Portability:** ✅ High (template file)
- **Implementation complexity:** N/A (template)

---

### 🎯 Frontend Design Skills

#### 16. frontend-design
- **What it does:** Creates distinctive, production-grade frontend interfaces with high design quality
- **Use cases:** Building web components, pages, applications with exceptional aesthetics
- **Dependencies:** HTML/CSS/JS, React, Vue support
- **Portability:** ✅ High (web-standard based)
- **Implementation complexity:** Medium-High
- **Note:** Avoids generic "AI slop" design patterns, generates creative polished code

---

## 🔧 How Skills Are Structured

### SKILL.md Format

Every skill is a folder containing a `SKILL.md` file with this structure:

```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it. Include triggers and contexts.
---

# My Skill Name

[Instructions that Claude follows when this skill is active]

## When to Use
- Trigger scenario 1
- Trigger scenario 2

## Examples
- Example usage 1
- Example usage 2

## Guidelines
- Guideline 1
- Guideline 2

## Tools Available
- Tool 1: Purpose
- Tool 2: Purpose

## Output Format
[Expected output structure]
```

### Key Components:

1. **YAML Frontmatter (Required):**
   - `name`: Unique lowercase identifier (hyphen-case, matches folder name)
   - `description`: Complete description of purpose, usage, and triggers

2. **Markdown Body:**
   - Instructions Claude follows
   - Examples demonstrating usage
   - Guidelines for proper execution
   - Tool specifications (if skill uses specific tools)
   - Output format expectations

### Critical Rule:

**The `description` field is the primary triggering mechanism.** Include all "when to use" information in the description, not just in the body.

**Example:**
```yaml
description: "Create animated GIFs optimized for Slack from descriptions like 'make me a GIF for Slack of X doing Y'. Use when users request animated GIFs or emoji animations for Slack."
```

---

## 📦 Installation Methods

### Method 1: Claude Code Plugin Installation

```bash
# Add the Anthropic skills marketplace (if not already added)
/plugin add-marketplace https://github.com/anthropics/skills

# Browse available skills
/plugin browse

# Install a specific skill
/plugin install example-skills:algorithmic-art
/plugin install document-skills:pdf
/plugin install example-skills:mcp-builder
```

### Method 2: Manual Installation to Project

1. **Create skill directory:**
   ```bash
   mkdir -p .claude/skills/my-custom-skill
   ```

2. **Create SKILL.md:**
   ```bash
   touch .claude/skills/my-custom-skill/SKILL.md
   ```

3. **Copy skill content from Anthropic repository:**
   - Visit: https://github.com/anthropics/skills/tree/main/skills/[skill-name]
   - Copy the SKILL.md content
   - Paste into your local SKILL.md file

4. **Customize for your project:**
   - Update description to match your use cases
   - Modify examples to fit your domain
   - Adjust guidelines for your team's standards

### Method 3: Create Custom Skill from Template

```bash
# Use the template-skill as a starting point
curl https://raw.githubusercontent.com/anthropics/skills/main/skills/template-skill/SKILL.md \
  -o .claude/skills/my-new-skill/SKILL.md

# Edit the SKILL.md file to customize
```

---

## 🚀 Implementing Skills in This Project

### Current Project Context:

**Project:** claude-code-project-template
**Tech Stack:** React (frontend) + FastAPI (backend)
**Agent System:** 15-agent orchestration with strict role boundaries

### Recommended Skills for This Project:

#### Tier 1: Immediate Value (Install Now)

1. **webapp-testing**
   - Why: Automated testing with Playwright aligns with @harshit-2.0 (Test Executor)
   - Agent: @harshit-2.0 should have access
   - Installation: `/plugin install example-skills:webapp-testing`

2. **mcp-builder**
   - Why: Creating MCP servers extends backend capabilities
   - Agent: @anand-2.0 (Code Executor) and @sama-2.0 (AI/ML Engineer)
   - Installation: `/plugin install example-skills:mcp-builder`

3. **frontend-design**
   - Why: Already installed, enforces high-quality frontend design
   - Agents: @hitesh-2.0 (Frontend Specialist), @varsha-2.0 (UI/UX Designer - read-only)
   - Status: ✅ Already installed

4. **docx / pdf / xlsx**
   - Why: Document generation for reports, exports, dashboards
   - Agents: @anand-2.0 (general), @hitesh-2.0 (PDF reports from frontend)
   - Installation: `/plugin install document-skills:pdf`, etc.

#### Tier 2: High Potential (Consider for Future)

5. **internal-comms**
   - Why: Standardize status reports, project updates
   - Agent: @documentation-manager could leverage this
   - Customization: Adapt to Vitraya's communication style

6. **theme-factory**
   - Why: Consistent styling across frontend artifacts
   - Agent: @varsha-2.0 (UI/UX Designer) for design systems
   - Customization: Add Vitraya brand themes

7. **algorithmic-art**
   - Why: Generative backgrounds, data visualizations
   - Agent: @hitesh-2.0 for unique UI elements

#### Tier 3: Niche Use Cases (Optional)

8. **slack-gif-creator**
   - Why: Team communication assets
   - Use case: Internal team culture, Slack workspace

9. **canvas-design**
   - Why: Marketing materials, posters
   - Use case: If project includes marketing collateral generation

---

## 🎯 Agent-Skill Mapping

### Which Agents Should Use Which Skills?

| Agent | Skills to Use | Rationale |
|-------|---------------|-----------|
| @anand-2.0 | mcp-builder, docx, pdf, xlsx, webapp-testing | Full-stack executor needs broad toolset |
| @hitesh-2.0 | **frontend-design**, theme-factory, algorithmic-art, pdf (reports) | Frontend specialist needs design tools |
| @varsha-2.0 | frontend-design (read-only), theme-factory, canvas-design | UI/UX designer explores aesthetics |
| @sama-2.0 | mcp-builder, docx (AI reports), xlsx (data analysis) | AI/ML engineer needs data + integration tools |
| @harshit-2.0 | **webapp-testing** | Test executor needs automated testing framework |
| @shawar-2.0 | mcp-builder (deployment integrations) | Deployment expert may need custom MCP servers |
| @documentation-manager | internal-comms, docx, pdf | Documentation lifecycle needs document tools |

---

## 📖 Best Practices for Skill Extraction

### 1. Start with High-Portability Skills

**Priority order:**
1. ✅ High portability + Low complexity: `slack-gif-creator`, `webapp-testing`, `internal-comms`
2. ✅ High portability + Medium complexity: `docx`, `pdf`, `xlsx`, `mcp-builder`
3. ⚠️ Medium portability + High complexity: `web-artifacts-builder`, `frontend-design`

### 2. Customize for Your Domain

**Don't just copy-paste.** Adapt skills to your project:

**Example: internal-comms**
```yaml
# Original description
description: "Write internal communications like status reports, newsletters, and FAQs"

# Customized for medical AI project
description: "Write internal communications for medical AI project: status reports following DPPM framework, HIPAA-compliant incident reports, clinical validation updates, and FDA submission documentation"
```

### 3. Integrate with Agent System

**Skills should align with agent boundaries:**

- **Orchestrators (Atharva, Bug-Fix-Orchestrator):** Use planning skills, not execution skills
- **Executors (Anand, Hitesh):** Use implementation skills (frontend-design, mcp-builder, docx/pdf/xlsx)
- **Validators (Ankur, Harshit):** Use testing/quality skills (webapp-testing)

### 4. Respect Licensing

**Document skills (docx, pdf, pptx, xlsx):**
- Source-available (not open source)
- Use for reference and inspiration
- Check Anthropic's terms before commercial use

**Example skills (algorithmic-art, mcp-builder, etc.):**
- Apache 2.0 license
- Free to use, modify, distribute

### 5. Version Control Skills

**Treat skills as code:**

```bash
# Add skill to git
git add .claude/skills/my-custom-skill/SKILL.md

# Commit with context
git commit -m "Add custom 'medical-report-generator' skill based on docx"

# Track changes over time
git log .claude/skills/my-custom-skill/SKILL.md
```

---

## 🔄 Skill Lifecycle Management

### Creating a Custom Skill (Step-by-Step)

**Example: Creating a "Medical Summary Generator" skill**

1. **Identify the need:**
   - User story: "As a clinician, I need to generate patient summaries from structured data"
   - Existing skill to adapt: `docx` (document generation)

2. **Create skill structure:**
   ```bash
   mkdir -p .claude/skills/medical-summary-generator
   cd .claude/skills/medical-summary-generator
   touch SKILL.md
   ```

3. **Write SKILL.md:**
   ```markdown
   ---
   name: medical-summary-generator
   description: "Generate HIPAA-compliant patient medical summaries from structured EMR data. Use when creating discharge summaries, referral documents, or clinical reports. Outputs DOCX format with proper medical terminology and formatting."
   ---

   # Medical Summary Generator

   Generate professional medical summaries from electronic medical record (EMR) data.

   ## When to Use
   - Creating discharge summaries
   - Generating referral documents
   - Producing clinical progress notes
   - Exporting patient summaries for care transitions

   ## Input Format
   Expects structured JSON with patient data:
   ```json
   {
     "patient_id": "string",
     "demographics": {...},
     "chief_complaint": "string",
     "history_of_present_illness": "string",
     "medications": [...],
     "allergies": [...],
     "vital_signs": {...},
     "assessment": "string",
     "plan": "string"
   }
   ```

   ## Output Format
   DOCX file with sections:
   - Patient Demographics
   - Chief Complaint
   - History of Present Illness
   - Medications & Allergies
   - Physical Examination
   - Assessment & Plan

   ## Guidelines
   - Use proper medical terminology
   - Follow HIPAA de-identification rules
   - Include disclaimers for AI-generated content
   - Validate medication names against drug databases
   - Flag missing critical information (allergies, medications)

   ## Tools Available
   - docx: Document creation with formatting
   - pdf: Export to PDF for finalized summaries
   - WebSearch: Validate medication names if needed

   ## Example Usage
   User: "Generate a discharge summary for patient MRN-12345"

   Agent:
   1. Retrieves patient data from EMR API
   2. Validates completeness (allergies, medications present)
   3. Generates DOCX with standard medical summary format
   4. Adds disclaimer: "AI-generated summary. Verify all information."
   5. Returns DOCX file for clinician review
   ```

4. **Test the skill:**
   ```bash
   # In Claude Code, invoke the skill
   # User: "Use medical-summary-generator to create a discharge summary"
   ```

5. **Iterate and improve:**
   - Collect feedback from @anand-2.0 or @sama-2.0 using the skill
   - Update SKILL.md based on edge cases
   - Version control changes

6. **Document in Agent Communication Board:**
   ```markdown
   ## ✅ Completed Today
   - **[SKILL-001]** Created medical-summary-generator skill – @anand-2.0 ✅ (2025-11-23 - Tested with 3 sample patients, works as expected)
   ```

---

## 📚 Learning Resources

### Official Resources:
- **Repository:** https://github.com/anthropics/skills
- **Blog Post:** https://www.anthropic.com/news/skills
- **Documentation:** https://deepwiki.com/anthropics/skills

### Community Resources:
- **Simon Willison's Analysis:** https://simonwillison.net/2025/Oct/16/claude-skills/
- **Community Guide:** https://karozieminski.substack.com/p/claude-skills-anthropic-viral-toolkit-agentic-workflows-community-guide

### Key Concepts:
1. **SKILL.md format specification:** https://deepwiki.com/anthropics/skills/2.2-skill.md-format-specification
2. **Quick Start Guide:** https://deepwiki.com/anthropics/skills/1.1-quick-start
3. **Document Skills Guide:** https://deepwiki.com/anthropics/skills/3.4-document-skills

---

## ✅ Action Items for This Project

### Immediate (This Week):
1. ✅ Install `webapp-testing` for @harshit-2.0
2. ✅ Install `mcp-builder` for @anand-2.0 and @sama-2.0
3. ✅ Verify `frontend-design` is properly configured for @hitesh-2.0

### Short-Term (This Month):
4. ⏳ Install document skills (pdf, docx, xlsx) for reporting
5. ⏳ Customize `internal-comms` for Vitraya's communication style
6. ⏳ Create custom skill: "medical-summary-generator" (if applicable to project domain)

### Long-Term (This Quarter):
7. 🔮 Explore `theme-factory` for design system consistency
8. 🔮 Evaluate `algorithmic-art` for unique UI elements
9. 🔮 Build custom MCP server using `mcp-builder` for EMR integration (if applicable)

---

## 🎯 Summary: Extractable Skills for Any Project

**Universal (Works Everywhere):**
- `webapp-testing` - Automated testing
- `mcp-builder` - API integrations
- `docx/pdf/xlsx` - Document generation
- `internal-comms` - Communication templates
- `frontend-design` - High-quality UI

**Domain-Specific (Adapt to Your Needs):**
- `brand-guidelines` - Replace with your brand
- `theme-factory` - Customize themes
- `slack-gif-creator` - Team culture (if using Slack)

**Creative (Niche Use Cases):**
- `algorithmic-art` - Generative visuals
- `canvas-design` - Marketing materials
- `web-artifacts-builder` - Complex React apps

**Meta (Skill Development):**
- `skill-creator` - Learn to create skills
- `template-skill` - Boilerplate for new skills

---

**Last Updated:** 2025-11-23
**Maintained By:** @documentation-manager
**Related Docs:**
- `.claude/docs/protocols/DELEGATION_PROTOCOL.md`
- `.claude/docs/methodologies/DPPM_FRAMEWORK.md`
- `AGENT_COMMUNICATION_BOARD.md`

---

## Sources:
- [GitHub - anthropics/skills: Public repository for Skills](https://github.com/anthropics/skills)
- [SKILL.md Format Specification | DeepWiki](https://deepwiki.com/anthropics/skills/2.2-skill.md-format-specification)
- [Introducing Agent Skills | Claude](https://www.anthropic.com/news/skills)
- [skills/README.md at main · anthropics/skills](https://github.com/anthropics/skills/blob/main/README.md)
- [skills/skill-creator/SKILL.md at main · anthropics/skills](https://github.com/anthropics/skills/blob/main/skill-creator/SKILL.md)
- [Quick Start | anthropics/skills | DeepWiki](https://deepwiki.com/anthropics/skills/1.1-quick-start)
- [Document Skills | DeepWiki](https://deepwiki.com/anthropics/skills/3.4-document-skills)
- [Claude Skills are awesome, maybe a bigger deal than MCP](https://simonwillison.net/2025/Oct/16/claude-skills/)
- [Anthropic's Claude Skills Are Taking the AI Community by Storm](https://karozieminski.substack.com/p/claude-skills-anthropic-viral-toolkit-agentic-workflows-community-guide)

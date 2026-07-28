# AI Test Agent Toolkit

**Created with:** GitHub Copilot (Claude Sonnet 4.6)

---

## Overview

This toolkit is a **GitHub Copilot Agent** with a set of structured **Skills** for VS Code.
Together they define a repeatable, step-by-step **AI-assisted test analysis workflow** for any
software development ticket tracked in JIRA.

The methodology — requirements analysis, BDD test planning, automation evaluation, regression
risk assessment — is project-agnostic and can be adapted to any tech stack.

---

## Repository Structure

```
AI-skills/
├── agents/
│   └── test-agent.agent.md          ← Agent orchestrator (main entry point)
├── skills/
│   ├── 01-requirements-analysis/
│   │   └── SKILL.md                 ← Extract requirements + verify implementation
│   ├── 02-unit-test-assessment/
│   │   └── SKILL.md                 ← Analyse unit test coverage
│   ├── 03-manual-test-plan/
│   │   └── SKILL.md                 ← Generate BDD test scenarios
│   ├── 04-automation-evaluation/
│   │   └── SKILL.md                 ← Evaluate automation justification
│   ├── 05-test-plan-output/
│   │   └── SKILL.md                 ← Generate test plan document + branch proposal
│   └── 06-regression-matrix/
│       └── SKILL.md                 ← Regression risk matrix (fully independent)
└── tools/
    ├── jira_tool.py                 ← Fetch ticket details, post comments
    ├── confluence_tool.py           ← Upload test plans to Confluence
    ├── run_pytest_with_html_report.sh ← Run automation tests and generate HTML report
    ├── .env.example                 ← Required environment variables
    └── README.md                    ← Setup and configuration guide
```

---

## Skill Dependencies

All skills can be **invoked independently** with only ticket context provided.
The agent orchestrates them in order for maximum completeness.

| Skill | Independent? | Notes |
|---|---|---|
| `test-agent` (agent) | ✅ Yes | Orchestrator — start here for every new ticket |
| `/01-requirements-analysis` | ✅ Yes | Needs ticket number only |
| `/02-unit-test-assessment` | ✅ Soft | Richer output when step 01 is done first |
| `/03-manual-test-plan` | ✅ Soft | Richer output when step 01 is done first |
| `/04-automation-evaluation` | ✅ Soft | Richer output when steps 01 + 03 are done first |
| `/06-regression-matrix` | ✅ Yes | Fully independent — can run at any point |
| `/05-test-plan-output` | ⚠️ Soft | Assembles all prior outputs — run last for best results |

> **Soft dependency** means: the skill checks for prior step output in the current session.
> If not found, it fetches ticket context independently and proceeds on its own.

---

## Purpose

Instead of writing ad hoc test plans or relying on memory for what to check, this toolkit ensures:

- Every ticket is analysed in the **same structured order**
- Nothing is skipped (negative paths, edge cases, regression impact)
- Output is consistent and ready to copy into Jira or share with the team
- Test plans and data files are saved locally in a predictable location
- The agent never takes destructive actions (no direct commits to `main`, no automatic Jira posts)

---

## Installation

### Personal use (available in all VS Code workspaces)

Copy the `agents/` and `skills/` folders to your user-level Copilot config:

```bash
# macOS / Linux
cp -r agents ~/.copilot/agents
cp -r skills ~/.copilot/skills

# Also copy the tools/ directory to your preferred scripts directory
cp -r tools <YOUR_SCRIPTS_DIR>/tools
```

### Workspace use (scoped to a single project)

Copy into your project's `.github/` folder:

```bash
cp -r agents .github/agents
cp -r skills .github/skills
```

---

## Configuration

Before using the toolkit, set these values in the `test-agent.agent.md` and in any skill you
invoke independently:

| Variable | Description | Example |
|---|---|---|
| `<SCRIPTS_DIR>` | Parent path containing your `tools/` folder | `/home/user/scripts` |
| `<OUTPUT_DIR>` | Path where test plan files are saved | `/home/user/scripts` |
| `<PROJECT_KEY>` | Your JIRA project key | `MYPROJECT` |
| `<CONFLUENCE_SPACE>` | Your Confluence space key | `TEAM` |

---

## How to Use

### Requirements

- VS Code with the **GitHub Copilot** extension installed and signed in
- Copilot Chat enabled (agent mode)

### Start the Workflow

1. Open any project in VS Code
2. Open Copilot Chat (`Ctrl+Alt+I` / `Cmd+Alt+I`) and switch to **Agent mode**
3. Select the `test-agent` from the agent picker, or type `/` to invoke individual skills
4. Provide the ticket number — context is fetched automatically via `jira_tool.py`

### Recommended Workflow per Ticket

```
test-agent                     ← start here (orchestrates steps below automatically)
  └── /01-requirements-analysis    ← step 1: extract requirements + verify implementation
  └── /02-unit-test-assessment     ← step 2: analyse unit test coverage
  └── /03-manual-test-plan         ← step 3: generate BDD test scenarios
  └── /04-automation-evaluation    ← step 4: evaluate automation justification
  └── /06-regression-matrix        ← step 5: regression risk matrix
  └── /05-test-plan-output         ← step 6: generate documents + branch proposal
```

Each skill can also be used **independently** — for example, running only `/06-regression-matrix`
on an existing ticket without going through the full flow.

---

## Adapting for Your Project

Update the following placeholders inside the files:

- **`<SCRIPTS_DIR>`** / **`<OUTPUT_DIR>`** — your local path to scripts and output
- **`<PROJECT_KEY>`** — your JIRA project key
- **`<CONFLUENCE_SPACE>`** — your Confluence space key
- **Technology stack** in `04-automation-evaluation/SKILL.md` — adapt to your cloud/infra
- **Branch naming conventions** in `05-test-plan-output/SKILL.md` — adapt to your project rules
- **Test data naming conventions** — define a pattern that suits your project

---

## Constraints and Safety Rules

The agent and all skills in this toolkit will never:

- Create test files without explicit instruction
- Commit directly to the `main` branch
- Skip steps or change their order
- Proceed without a ticket number
- Post a Jira comment before all testing is complete and the test plan has been uploaded to Confluence

Jira ticket details (title, description, comments) are fetched automatically via `jira_tool.py` —
the user only needs to provide the ticket number.

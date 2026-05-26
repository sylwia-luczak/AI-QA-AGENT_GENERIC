# AI Test Agent Prompt Toolkit

**Author:** Sylwia Łuczak-Jagiela
**Created with:** GitHub Copilot (Claude Sonnet 4.6)

---

## Overview

This toolkit is a set of structured prompt files for VS Code's GitHub Copilot agent.
Together they define a repeatable, step-by-step **AI-assisted test analysis workflow** for software development tickets.

The workflow was originally designed for the **FTRS (Find the Right Service)** project at NHS England,
but the underlying methodology — requirements analysis, BDD test planning, automation evaluation,
regression risk assessment — applies to any software project.

> **Note on naming:** The `ftrs-` prefix in filenames reflects the original project context.
> When adapting this toolkit for a different project, rename the files accordingly
> (e.g., `myproject-test-agent.prompt.md`) and update project-specific references inside each file
> (save paths, naming conventions, technology stack).

---

## Purpose

Instead of writing ad hoc test plans or relying on memory for what to check, this toolkit ensures that:

- Every ticket is analysed in the **same structured order**
- Nothing is skipped (negative paths, edge cases, regression impact)
- Output is consistent and ready to copy into Jira or share with the team
- Test plans and SQL data files are saved locally in a predictable location
- The agent never takes destructive actions (no direct commits to `main`, no automatic Jira posts)

---

## Files

| File | Slash Command | Purpose |
|---|---|---|
| `ftrs-test-agent.prompt.md` | `/ftrs-test-agent` | **Main entry point.** Defines the agent role, constraints, initialization flow, and the full ordered execution sequence. Start here for every new ticket. |
| `ftrs-requirements-analysis.prompt.md` | `/ftrs-requirements-analysis` | **Steps 1–2.** Extracts and structures functional and non-functional requirements from the ticket. Then verifies whether the implementation on `main` matches those requirements and reports discrepancies. |
| `ftrs-unit-test-assessment.prompt.md` | `/ftrs-unit-test-assessment` | **Step 3.** Analyses existing unit tests: coverage, negative scenarios, edge cases, failure modes, mock appropriateness. Identifies gaps and recommends improvements. |
| `ftrs-manual-test-plan.prompt.md` | `/ftrs-manual-test-plan` | **Step 4.** Generates manual test scenarios in BDD format (GIVEN / WHEN / THEN) covering happy path, negative scenarios, validation errors, feature flag states, and regression scenarios. |
| `ftrs-automation-evaluation.prompt.md` | `/ftrs-automation-evaluation` | **Step 5.** Evaluates whether automated integration tests are justified. If yes, proposes test scope, structure, mocking strategy, CI impact, and example Gherkin scenarios using Python / Playwright / AWS. |
| `ftrs-test-plan-output.prompt.md` | `/ftrs-test-plan-output` | **Steps 6–7.** Generates the final `FTRS-XXXX_test_plan.md` document and (if applicable) `FTRS-XXXX_test_data.sql`. Also proposes a valid git branch name following project conventions. |
| `ftrs-regression-matrix.prompt.md` | `/ftrs-regression-matrix` | **Regression Risk Matrix.** Evaluates risk across 13 system areas (API, Lambda, Feature Flags, Database, Auth, CI/CD, etc.) and classifies each as LOW / MEDIUM / HIGH / CRITICAL. Mandatory in every test plan. |

---

## How to Use

### Requirements

- VS Code with the **GitHub Copilot** extension installed and signed in
- Copilot Chat enabled (agent mode)

### Usage in Any Project

Because these files are stored at the **user profile level**, they are available in every VS Code workspace automatically — no per-project setup is required.

1. Open any project in VS Code
2. Open Copilot Chat (`Ctrl+Alt+I` / `Cmd+Alt+I`) and switch to **Agent mode**
3. Type `/` — the `ftrs-*` prompts will appear in the command list
4. Select `/ftrs-test-agent` to start the workflow

### Recommended Workflow per Ticket

```
/ftrs-test-agent                  ← start here, provide ticket number (description is auto-fetched via jira_tool.py)
/ftrs-requirements-analysis       ← steps 1–2
/ftrs-unit-test-assessment        ← step 3
/ftrs-manual-test-plan            ← step 4
/ftrs-automation-evaluation       ← step 5
/ftrs-test-plan-output            ← steps 6–7 (generates documents)
/ftrs-regression-matrix           ← included in the output document, can be run separately
```

Each prompt can also be used **independently** — for example, running only `/ftrs-regression-matrix`
on an existing ticket without going through the full flow.

---

## Adapting for a Different Project

To reuse this toolkit in a different project context:

1. Copy all files and rename them (e.g., replace `ftrs-` with your project prefix)
2. Update the following project-specific references inside the files:
   - **Save path** in `ftrs-test-plan-output.prompt.md` (currently `/Users/sylwia.luczak-jagiela/scripts`)
   - **File naming convention** (currently `FTRS-XXXX_test_plan.md`)
   - **Branch naming rules** (currently `task/FTRS-XXXX-description`)
   - **Technology stack** in `ftrs-automation-evaluation.prompt.md`
   - **Test data naming conventions** (OldDOS service ID patterns)

---

## Constraints and Safety Rules

The agent operating under this toolkit will never:

- Create test files without explicit instruction
- Commit directly to the `main` branch
- Skip steps or change their order
- Proceed without a ticket number
- Post a Jira comment before all testing is complete and the test plan has been uploaded to Confluence

Jira ticket details (title, description, comments) are fetched automatically via `jira_tool.py` — the user only needs to provide the ticket number.

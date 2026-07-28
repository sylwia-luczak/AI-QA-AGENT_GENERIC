---
name: config
description: 'Shared configuration for all AI Test Agent skills. Defines environment-specific paths, project keys, and tool commands. Load this skill first (or configure values here once) to resolve all <VARIABLE> references used across the toolkit. Update this file when changing machines, projects, or output directories.'
---

# AI Test Agent — Shared Configuration

> ⚙️ This file is the single source of truth for all environment-specific values used across the toolkit.
> When you encounter `<VARIABLE>` in any skill or agent file, substitute the value from the table below.

---

## Variables

| Variable | Value | Description |
|---|---|---|
| `<SCRIPTS_DIR>` | `/your/path/to/scripts` | Parent directory containing the `tools/` folder |
| `<OUTPUT_DIR>` | `/your/path/to/output` | Directory where test plan `.md` and `.sql` files are saved |
| `<PROJECT_KEY>` | `MYPROJECT` | Your JIRA project key (e.g. `MYPROJECT`) |
| `<CONFLUENCE_SPACE>` | `TEAM` | Your Confluence space key |

---

## How to Update

To adapt the toolkit to your environment or project:

1. Edit **this file only** — update the relevant row in the table above
2. All skills will automatically use the new value via `<VARIABLE>` substitution
3. Do **not** edit individual skill files to change paths or project keys

---

## Tool Commands (resolved)

Once configured, the tool commands used across skills will resolve to:

| Command | Resolved value |
|---|---|
| Fetch JIRA ticket | `python <SCRIPTS_DIR>/tools/jira_tool.py fetch <TICKET_NUMBER>` |
| Post JIRA comment | `python <SCRIPTS_DIR>/tools/jira_tool.py comment <TICKET> --file <OUTPUT_DIR>/<TICKET>_comment.md` |
| Find Confluence page | `python <SCRIPTS_DIR>/tools/confluence_tool.py find --space <CONFLUENCE_SPACE> "<TICKET>"` |
| Upload to Confluence | `python <SCRIPTS_DIR>/tools/confluence_tool.py update <PAGE_ID> --file <OUTPUT_DIR>/<TICKET>_test_plan.md` |
| Run pytest + HTML report | `bash <SCRIPTS_DIR>/tools/run_pytest_with_html_report.sh` |

---

## Notes

- `<OUTPUT_DIR>` and `<SCRIPTS_DIR>` can point to the same directory if you keep tools and output together
- See `tools/README.md` for setup instructions and required environment variables (`.env`)

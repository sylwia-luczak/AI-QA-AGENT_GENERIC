# Jira Tool

A Python CLI tool for interacting with Jira Server / Data Center via Personal Access Token (PAT).

## Features

- Fetch full ticket details: summary, description, status, comments, subtasks, linked issues
- Post a comment to a ticket (inline text or from a file)

## Setup

### 1. Install dependencies

```bash
pip install requests python-dotenv
```

Or if using `uv`:

```bash
uv pip install requests python-dotenv
```

### 2. Configure credentials

```bash
cp .env.example .env
```

Edit `.env` and fill in:

```
JIRA_BASE_URL=https://jira.your-organisation.net
JIRA_PAT=your_personal_access_token_here
```

**Never commit `.env` to version control.**

### How to generate a Personal Access Token in Jira

1. Log in to Jira
2. Go to your **Profile** (top-right avatar)
3. Click **Personal Access Tokens**
4. Click **Create token**
5. Give it a name (e.g., `jira-cli-tool`) and set an expiry date
6. Copy the token and paste it into `.env` as `JIRA_PAT`

---

## Usage

### Fetch a ticket

```bash
python jira_tool.py fetch FTRS-1234
```

Displays:
- Title, type, status, priority, assignee, reporter, labels
- Full description
- Subtasks with status
- Linked issues
- All comments with author and date

### Post a comment (inline)

```bash
python jira_tool.py comment FTRS-1234 "Testing completed. All scenarios passed."
```

### Post a comment from a file

```bash
python jira_tool.py comment FTRS-1234 --file /Users/sylwia/scripts/FTRS-1234_comment.md
```

This is useful when the comment was prepared by the AI agent and saved to a file.

---

## Corporate SSL certificates

If you get SSL errors, the tool automatically picks up the cert bundle from the
`NODE_EXTRA_CA_CERTS` environment variable (already configured in `~/.zshrc`).
No extra configuration needed.

---

## Security notes

- The PAT is read from the `.env` file — it is never hardcoded
- The `.env` file must be kept local and not committed to any repository
- PAT permissions needed: **Browse Projects**, **Add Comments**
- Set a reasonable expiry date on your token and rotate it periodically

---
name: ftrs-test-plan-output
description: >
  FTRS Step 6 & 7 — Test Plan Document Output and Branch Creation. Use after completing all analysis
  steps for a FTRS JIRA ticket. Generates the final structured test plan markdown document and
  (if required) a SQL data file with test data. Also proposes a valid git branch name if automation
  is required. Files are saved to /Users/sylwia.luczak-jagiela/scripts.
  Keywords: test plan document, generate test plan, save test plan, SQL test data, branch name,
  FTRS output, FTRS-XXXX_test_plan.md, FTRS-XXXX_test_data.sql.
mode: agent
---

# FTRS — Step 6️⃣ & 7️⃣: Test Plan Output + Branch Creation

---

## 6️⃣ Generate Test Plan Document

Generate a structured test plan document and (if required) a SQL data file.

### Save Location
```
/Users/sylwia.luczak-jagiela/scripts
```

### File Naming Convention
```
FTRS-0000_test_plan.md
FTRS-0000_test_data.sql
```
Replace `0000` with the actual ticket number.

---

### Test Plan Document Structure

The `FTRS-XXXX_test_plan.md` must include all of the following sections:

1. **Summary** — brief description of what this ticket does and test scope
2. **Risk Assessment** — key risks identified
3. **Requirements Breakdown** — structured list of functional and non-functional requirements
4. **Manual BDD Scenarios** — all scenarios from Step 4
5. **Automation Recommendation** — justified recommendation from Step 5
6. **Regression Impact** — areas at risk of regression
7. **Environment Impact** — any environment-specific concerns
8. **Open Questions** — unresolved ambiguities or missing acceptance criteria
9. **Regression Risk Matrix** — full matrix from Step 7 (see `/ftrs-regression-matrix`)

---

### SQL Data File

If test scenarios require creating services in OldDOS, include all `INSERT` statements in `FTRS-XXXX_test_data.sql`.

Apply naming conventions:
- GP Practice IDs: `9XXXX0Y`
- Pharmacy IDs: `8XXXX0Y`
- Natural names — no ticket numbers in service names, minimal use of "TEST"

---

## 📤 After Generating the Documents

Once the files are saved, offer the following actions:

### Post comment to Jira

Prepare a short summary comment (what was analysed, what scenarios were written, any risks identified) and offer to post it:

```bash
python /Users/sylwia.luczak-jagiela/scripts/jira/jira_tool.py comment FTRS-XXXX --file /Users/sylwia.luczak-jagiela/scripts/FTRS-XXXX_comment.md
```

### Upload test plan to Confluence

Ask the user for the Confluence page ID (or find it automatically):

```bash
# Find page by ticket number
python /Users/sylwia.luczak-jagiela/scripts/jira/confluence_tool.py find --space DR "FTRS-XXXX"

# Upload the test plan
python /Users/sylwia.luczak-jagiela/scripts/jira/confluence_tool.py update <PAGE_ID> --file /Users/sylwia.luczak-jagiela/scripts/FTRS-XXXX_test_plan.md
```

❗ Always confirm with the user before posting to Jira or Confluence.

---

## 📋 Confluence Page Structure — Manual Test Scenarios

The Confluence page must contain **only manual test scenarios and their execution results**.
No analysis summaries, requirement breakdowns, risk descriptions, or other content from the local test plan document.

### Scenario Header

Every scenario uses an **H3 heading** formatted as:

```
Test Scenario 01 — <Scenario Title>
```

- The heading text must be coloured **blue** (Confluence colour: `rgb(0,82,204)`)
- Number is always zero-padded and sequential: `01`, `02`, `03`, …
- Title is taken from the BDD scenario name

### Steps Format

Steps are written in **GIVEN / WHEN / THEN** format:

- The words **GIVEN**, **WHEN**, **THEN** (and **AND**) are always **bold**
- Step text is black (no colour styling)
- Each step is on its own line
- After each step, include an **empty line** as a placeholder for a screenshot or evidence

Example structure:
```
**GIVEN** <precondition>

**WHEN** <action>

**THEN** <expected result>

**AND** <additional assertion>

```

### Verification Code Snippets

If a step requires verification via AWS CLI, SQL, or an API call, include the relevant code snippet directly in the scenario — inline after the relevant THEN/AND step, inside a Confluence `code` block.

### Results Section

After the last step of each scenario, include only:

```
*Result:*
*Status:* PASS / FAIL / BLOCKED
*Notes:*
```

No other content after the results block.

### What Must NOT Appear on the Confluence Page

- Requirements breakdowns
- Risk assessments
- Automation recommendations
- Regression matrices
- Open questions
- Any narrative text not part of a test step or result

---

## 7️⃣ Branch Creation (If Automation Required)

If automated tests will be implemented, propose a valid branch name.

### Branch Naming Format
```
<branch-type>/FTRS-XXXX-<description>
```

### Rules

| Element | Requirement |
|---|---|
| Branch type | `task/` or `hotfix/` |
| JIRA reference | `FTRS-1234` (case insensitive) |
| Separator | `-` (hyphen) or `_` (underscore) |
| Description | Min 10 chars, max 45 chars, starts with alphanumeric, only letters/digits/`-`/`_` |

### Example
```
task/FTRS-1587-add_feature_flag_tests
```

### Agent Must:
1. Propose a valid branch name
2. Explain why it follows the conventions
3. Outline the folder structure for new tests
4. Confirm naming compliance explicitly

---

## 8️⃣ Run Service Automation Tests

After the test plan is generated, offer to run the existing service automation tests against the `internal-dev` environment.

### Marker Selection

Based on the ticket scope, determine which markers are relevant:

| Service Area | Marker |
|---|---|
| Organisation CRUD API | `crud-org-api` |
| Healthcare Service CRUD API | `crud-healthcare-service-api` |
| Location CRUD API | `crud-location-api` |

**Rules:**
- If the ticket touches the shared data layer (`ftrs_data_layer`, `DynamoDBRepository`, entity repositories) — run **all three** markers
- If the ticket touches a single service — run only the relevant marker(s)
- If the ticket is data-migration or dos-search only — skip CRUD markers; note that no service automation coverage exists for that area

### Run the Tests

```bash
/Users/sylwia.luczak-jagiela/scripts/run_pytest_with_html_report.sh "<markers>"
```

Examples:

```bash
# All CRUD APIs (data layer tickets)
/Users/sylwia.luczak-jagiela/scripts/run_pytest_with_html_report.sh "crud-org-api crud-healthcare-service-api crud-location-api"

# Organisation only
/Users/sylwia.luczak-jagiela/scripts/run_pytest_with_html_report.sh "crud-org-api"
```

The script will:
1. Clean `allure-results/` and `allure-reports/`
2. Run `make test MARKERS="..."` inside `tests/service_automation/`
3. Generate a self-contained `allure-reports/index.html`
4. Open the report in the browser automatically

### After Running

- Report the number of tests passed / failed per marker
- Note the path to the Allure report: `tests/service_automation/allure-reports/index.html`
- If any tests **failed**: list the failing test names and investigate before closing the ticket
- If all tests **passed**: confirm regression is clean and include the result summary in the Jira comment

❗ Always confirm with the user before running tests — they require an active AWS SSO session (`aws sso login --profile default`).

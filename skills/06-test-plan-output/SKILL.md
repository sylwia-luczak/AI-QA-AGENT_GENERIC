---
name: 05-test-plan-output
description: >
  Step 5 & 6 — Test Plan Document Output and Branch Creation. Generates the final structured
  test plan markdown document and (if required) a file with test data SQL statements.
  Also proposes a valid git branch name if automation is required, and offers to run existing
  automation tests against the target environment.
  Soft dependency on steps 01-04 and 06 — assembles their outputs into the final document.
  Can be run independently but produces the most complete output when all prior steps are done.
  Files are saved to <OUTPUT_DIR> (configure to your local path).
  Keywords: test plan document, generate test plan, save test plan, SQL test data, branch name,
  test plan output, Confluence upload, Jira comment, run tests, automation run.
argument-hint: '<PROJECT_KEY>-<TICKET_NUMBER>'
---

# Step 05 & 06: Test Plan Output + Branch Creation

## Dependency
**Soft dependency on steps 01–04 and 06.** Assembles all prior step outputs into the final
document. If some steps have not been completed, note the gaps and generate the document with
available information. If no prior steps are available, fetch ticket context first:
```bash
python <SCRIPTS_DIR>/tools/jira_tool.py fetch <TICKET_NUMBER>
```

---

## Step 5 — Generate Test Plan Document

Generate a structured test plan document and (if required) a test data SQL file.

### Save Location
```
<OUTPUT_DIR>
```
> Configure `<OUTPUT_DIR>` to your local output path (e.g., `/home/user/scripts`).

### File Naming Convention
```
<TICKET>_test_plan.md
<TICKET>_test_data.sql
```
Replace `<TICKET>` with the actual ticket number (e.g., `PROJECT-1234`).

---

### Test Plan Document Structure

The `<TICKET>_test_plan.md` must include all of the following sections:

1. **Summary** — brief description of what this ticket does and the test scope
2. **QA Summary Table** — one-glance rollup: ticket number, overall risk level (from step 06 regression matrix), automation recommendation (step 04), unit test coverage verdict (step 02), manual test result if already executed
3. **Risk Assessment** — key risks identified
4. **Requirements Breakdown** — structured list of functional (`FR1`, `FR2`, …) and non-functional (`NFR1`, `NFR2`, …) requirements, using the same IDs assigned in step 01
5. **Manual BDD Scenarios** — all scenarios from step 03, each tagged with the requirement ID(s) it covers
6. **Automation Recommendation** — justified recommendation from step 04
7. **Regression Impact** — areas at risk of regression
8. **Environment Impact** — any environment-specific concerns
9. **Open Questions** — unresolved ambiguities or missing acceptance criteria
10. **Regression Risk Matrix** — full matrix from step 06 (`/06-regression-matrix`)

---

### QA Summary Table

Include this table at the top of the test plan document and repeat it in chat as a quick
rollup once the pipeline finishes:

| Ticket | Risk Level | Automation Recommendation | Unit Test Coverage | Manual Test Result |
|---|---|---|---|---|
| `<TICKET>` | (highest level from step 06 matrix) | (from step 04) | (verdict from step 02) | PASS / FAIL / BLOCKED / Not yet executed |

---

### Test Data File

If test scenarios require creating test data, include all relevant `INSERT` statements in
`<TICKET>_test_data.sql`.

Apply consistent naming:
- Use a pattern linking IDs to the ticket number for traceability
- Use natural, realistic names — avoid ticket numbers in display names and excessive "TEST" prefixes

---

## After Generating the Documents

Once files are saved, offer the following actions:

### Post comment to Jira

Prepare a short summary comment as plain text in the chat. This applies whether the comment
follows the full pipeline or is requested standalone (e.g. the user ran manual tests
themselves and reports the results for a comment).

#### Comment Content

The comment must include:

1. **Manual test results** — summary of scenarios executed and their outcome (PASS / FAIL / BLOCKED)
2. **Confluence link** — link to the page with full scenario evidence
3. **PR link** — if automation tests were added or updated as part of this ticket
4. **Unit & integration test coverage** — a short note confirming this functionality is also covered
   by unit/integration tests, using the step 02 (`02-unit-test-assessment`) verdict. Where available,
   state how many tests cover it and briefly what they cover (e.g. "3 unit tests covering validation,
   mapping, and the feature-flag OFF path"). This is added value surfaced from the requirements
   analysis (steps 01) and unit test assessment (step 02) — it gives reviewers a complete picture of
   test coverage, not just the manual scenarios. If step 02 was not run in this session, omit this
   point rather than guessing.

Follow the **Jira Comment Approval Flow**:
1. Draft the comment and show it in the chat.
2. Ask explicitly: "Do you approve this comment? Should I post it to `<TICKET>`?"
3. Only after an explicit, affirmative confirmation, post it:
   ```bash
   python <SCRIPTS_DIR>/tools/jira_tool.py comment <TICKET> --file <OUTPUT_DIR>/<TICKET>_comment.md
   ```
4. Confirm to the user once posted.

❗ Never post without having just received explicit approval for that exact comment.

### Upload test plan to Confluence
```bash
# Find page by ticket number
python <SCRIPTS_DIR>/tools/confluence_tool.py find --space <CONFLUENCE_SPACE> "<TICKET>"

# Upload the test plan
python <SCRIPTS_DIR>/tools/confluence_tool.py update <PAGE_ID> --file <OUTPUT_DIR>/<TICKET>_test_plan.md
```

Always confirm with the user before posting to Jira or Confluence.

> For full Confluence page formatting requirements (scenario headers, step format, results section),
> see [confluence-format.md](./references/confluence-format.md).

---

## Step 6 — Branch Creation (If Automation Required)

If automated tests will be implemented, propose a valid branch name.

### Branch Naming Format
```
<branch-type>/<TICKET>-<description>
```

### Rules

| Element | Requirement |
|---|---|
| Branch type | e.g., `task/`, `feature/`, `hotfix/` — follow your project conventions |
| Ticket reference | `<PROJECT_KEY>-1234` |
| Separator | `-` (hyphen) or `_` (underscore) |
| Description | Min 10 chars, max 45 chars, starts with alphanumeric, only letters/digits/`-`/`_` |

### Example
```
task/PROJECT-1234-add_feature_flag_tests
```

The agent must:
1. Propose a valid branch name
2. Explain why it follows the conventions
3. Outline the folder structure for new tests
4. Confirm naming compliance explicitly

---

## Step 7 — Run Automation Tests (Optional)

After the test plan is generated, offer to run the existing automation test suite against the
target environment.

### Marker / Suite Selection

Based on the ticket scope, determine which test markers or suites are relevant:
- If the ticket touches shared/core components — run all relevant markers
- If the ticket touches a single area — run only the relevant marker(s)
- If no automation coverage exists for the affected area — note this explicitly

### Run the Tests
```bash
<SCRIPTS_DIR>/tools/run_pytest_with_html_report.sh "<markers>"
```

The script will:
1. Clean previous test results
2. Run tests with the specified markers
3. Generate a self-contained HTML report

### After Running
- Report the number of tests passed / failed per marker
- Note the path to the generated test report
- If any tests **failed**: list the failing test names and investigate before closing the ticket
- If all tests **passed**: confirm regression is clean and include the result summary in the Jira comment

Always confirm with the user before running tests — they may require authentication (e.g., SSO login,
cloud credentials) before execution.

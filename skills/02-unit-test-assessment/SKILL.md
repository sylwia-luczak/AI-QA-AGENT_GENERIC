---
name: 02-unit-test-assessment
description: >
  Step 2 — Unit Test Assessment. Analyses existing unit tests in the codebase relevant to a
  JIRA ticket. Evaluates coverage of functional requirements, negative scenarios, edge cases,
  failure modes, mock usage, and over-mocking. Identifies coverage gaps and recommends improvements.
  Can be used independently — requires ticket context and codebase access.
  Soft dependency on step 01-requirements-analysis (uses structured requirements for coverage check;
  will derive requirements from ticket if step 01 output is not available).
  Keywords: unit tests, test coverage, mocks, negative scenarios, edge cases, coverage gaps, unit testing,
  test assessment, mock strategy, over-mocking.
argument-hint: '<PROJECT_KEY>-<TICKET_NUMBER>'
---

# Step 02: Unit Test Assessment

## Dependency
**Soft dependency on step 01.** If requirements analysis output is available in this session,
use it to assess coverage. If not, derive requirements from the ticket directly:
```bash
python <SCRIPTS_DIR>/tools/jira_tool.py fetch <TICKET_NUMBER>
```

> **Role boundary:** Unit tests are written and executed by the **developer**. The tester's role
> is to verify that tests **exist** and **cover the acceptance criteria** — not to write or run
> them locally.

---

## Assessment Checklist

Answer each question explicitly for the ticket in scope:

- Are unit tests present for the changed code?
- Do they cover all functional requirements from the ACs?
- Do they include negative scenarios?
- Do they include edge cases?
- Do they test failure modes?
- Are mocks used appropriately (at system boundaries, not implementation details)?
- Is there over-mocking (mocking things that should be real)?
- Is the happy path the only path tested?

---

## Output

1. **Coverage gaps** — list any untested scenarios with specific references to requirements, using the `FR`/`NFR` IDs from step 01 wherever the gap maps to a specific requirement
2. **Recommendations** — specific improvements with justification
3. **Summary verdict** — one of:
   - ✅ **Pass** — adequate coverage found
   - ⚠️ **Needs Improvement** — gaps exist but not critical
   - ❌ **Insufficient** — significant gaps, action required before sign-off

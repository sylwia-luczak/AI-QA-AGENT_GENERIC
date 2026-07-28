---
name: 03-manual-test-plan
description: >
  Step 3 — Manual Test Plan in BDD format. Generates structured Gherkin-style GIVEN/WHEN/THEN
  test scenarios covering: happy path, negative scenarios, validation errors, permission scenarios,
  feature flag ON/OFF states, regression scenarios, and environment-specific behaviour.
  Ensures clarity, reproducibility, and deterministic expected results.
  Can be used independently — requires only ticket context.
  Soft dependency on step 01-requirements-analysis (uses structured requirements to generate
  scenarios; will derive requirements from ticket if step 01 output is not available).
  Keywords: BDD, manual testing, Gherkin, GIVEN WHEN THEN, test scenarios, happy path,
  negative testing, feature flags, manual test plan, test scenarios, BDD format.
argument-hint: '<PROJECT_KEY>-<TICKET_NUMBER>'
---

# Step 03: Manual Test Plan (BDD Format)

## Dependency
**Soft dependency on step 01.** Uses structured requirements to drive scenario generation.
If step 01 output is not available in this session, fetch ticket context directly:
```bash
python <SCRIPTS_DIR>/tools/jira_tool.py fetch <TICKET_NUMBER>
```

---

## Scenario Format

```
GIVEN <precondition>
WHEN <action>
THEN <expected result>
AND <additional assertion>
```

---

## Required Scenario Coverage

Include scenarios for each of the following (where applicable):

- ✅ Happy path scenarios
- ❌ Negative scenarios
- ⚠️ Validation errors
- 🔐 Permission scenarios (if applicable)
- 🚩 Feature flag ON state
- 🚩 Feature flag OFF state
- 🔄 Regression scenarios (existing behaviour that must not break)
- 🌍 Environment-specific behaviour (if applicable)

---

## Quality Criteria

Each scenario must be:
- **Clear** — unambiguous preconditions and expected results
- **Reproducible** — can be run by anyone with access to the environment
- **Deterministic** — the same input always produces the same output

---

## Example

**Test Scenario 01: Validate entity type mapping**
**Tags:** `@critical` `@validation`

```gherkin
GIVEN a "<entity_type>" record exists in the source system
WHEN the processing pipeline is triggered
THEN the record is created in the target system with the correct type mapping
AND the audit log confirms successful transformation
```

---

## Naming Convention for Test Data

When test scenarios require creating test data:

- Use a consistent prefix or pattern linking test data to the ticket number
- Use natural, realistic names — avoid embedding ticket numbers in display names
- Avoid excessive use of "TEST" in data values
- Document the naming convention in the test plan so any team member can reproduce the data

---

## Output

A numbered list of BDD scenarios tagged by category (happy path, negative, regression, etc.),
ready to be included in the test plan document and uploaded to Confluence.

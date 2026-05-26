---
name: ftrs-manual-test-plan
description: >
  FTRS Step 4 — Manual Test Plan in BDD format. Use after unit test assessment for a FTRS JIRA ticket.
  Generates structured Gherkin-style GIVEN/WHEN/THEN test scenarios covering: happy path, negative scenarios,
  validation errors, permission scenarios, feature flag ON/OFF states, regression scenarios,
  and environment-specific behaviour. Ensures clarity, reproducibility, and deterministic expected results.
  Keywords: BDD, manual testing, Gherkin, GIVEN WHEN THEN, test scenarios, happy path, negative testing,
  feature flags, FTRS manual test plan.
mode: agent
---

# FTRS — Step 4️⃣: Manual Test Plan (BDD Format)

Prepare structured test scenarios using BDD format.

---

## Format

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

**Test Scenario 01: Validate Community Pharmacy Organisation Type Name**
**Tags:** `@critical` `@bug-validation`

```gherkin
GIVEN a Community Pharmacy service (type 13) exists in old DoS database
WHEN I trigger migration via AWS Lambda queue-populator
THEN the organisation is created in DynamoDB with type = "Community Pharmacy"
AND CloudWatch logs show successful transformation
```

---

## Naming Convention for Test Data (OldDOS Services)

When test scenarios require creating services in OldDOS via DBeaver/SQL:

- **GP Practice IDs**: `9XXXX0Y` — where `XXXX` = ticket number, `Y` = scenario number
- **Pharmacy IDs**: `8XXXX0Y` — where `XXXX` = ticket number, `Y` = scenario number
- Names (publicname, address, etc.) should be natural — avoid ticket numbers in names and excessive use of "TEST"

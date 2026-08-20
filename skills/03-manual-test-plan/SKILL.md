---
name: 03-manual-test-plan
description: >
  Step 3 — Manual Test Plan in BDD format. Generates a lean set of Gherkin-style GIVEN/WHEN/THEN
  test scenarios that avoid duplicating unit/integration test coverage, focusing instead on
  edge cases, business-level acceptance, cross-service behaviour, and system-wide impact.
  Ensures clarity, reproducibility, and deterministic expected results.
  Can be used independently — requires only ticket context.
  Soft dependency on step 01-requirements-analysis (uses structured requirements to generate
  scenarios; will derive requirements from ticket if step 01 output is not available) and
  step 02-unit-test-assessment (uses its coverage verdict to avoid duplicating unit test scenarios).
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

**Soft dependency on step 02.** If a unit test assessment (coverage verdict + gaps) is available
in this session, use it to apply the Deduplication Rule below. If not available, proceed but
favour cross-boundary and business-level scenarios over pure logic checks.

---

## Core Principle

Manual scenarios exist to catch what unit and integration tests **cannot** — real business
outcomes, cross-service behaviour, and edge cases that only surface with live data and
infrastructure. They are not a re-run of unit test logic in Gherkin syntax.

> A simple ticket with 3 ACs, all already covered by passing unit tests, should produce
> **2–4 manual scenarios** — not one scenario per AC.

---

## Deduplication Rule (Apply Before Writing Any Scenario)

Before drafting scenarios, re-read the **step 02 output** (`02-unit-test-assessment`) for this
ticket, if available.

For each functional requirement or AC (use the `FR`/`NFR` IDs assigned in step 01), apply this filter:

| Question | If YES → | If NO →|
|---|---|---|
| Is this AC already fully covered by a **passing** unit test (per step 02 verdict), with no coverage gap? | **Skip** a dedicated manual scenario for it, or fold it into a broader end-to-end scenario | Include a manual scenario |
| Does validating this AC require crossing a real boundary (API contract, service call, database, queue/event, feature flag at runtime, real environment config)? | Include a manual scenario regardless of unit coverage | Lower priority for a dedicated scenario |
| Is this a pure internal logic/branching check (e.g. input validation, calculation, mapping) with no system-level consequence? | **Skip** — unit tests own this | — |
| Does step 02 flag this as a coverage gap, over-mocked, or untested edge case? | Include a manual scenario — this is exactly what manual testing must catch | — |

❗ Never delete manual coverage of HIGH/CRITICAL risk areas, feature flag ON/OFF states, or
cross-service data flows purely to reduce scenario count — the goal is to cut **redundant**
scenarios, not risk coverage.

---

## What Manual Testing Should Focus On

- 🧩 **Business-level acceptance** — does the end result match what the business actually asked for, not just what the function returns
- 🔗 **Cross-service / system behaviour** — end-to-end flow across services, not a single function
- 🌍 **Real environment edge cases** — data quirks, legacy records, migration artefacts that unit test fixtures don't reproduce
- 🚩 **Feature flag ON/OFF at runtime** — actual toggled behaviour in a live environment
- 🔄 **Regression on existing behaviour** — especially anything flagged HIGH/CRITICAL
- ❌ **Failure modes that depend on real infrastructure** — timeouts, malformed upstream data, partial failures

## What to Avoid

- One scenario per AC when several ACs are exercised by the same business flow — merge them into a single end-to-end scenario with multiple `AND` assertions
- Re-asserting pure validation/calculation logic that step 02 already confirmed is unit-tested and passing
- Padding the plan with scenarios that add no new risk coverage, just to look thorough

---

## Scenario Format

```
GIVEN <precondition>
WHEN <action>
THEN <expected result>
AND <additional assertion>
```

---

## Scenario Categories (Apply Selectively, Not as a Checklist)

For each category below, apply the Deduplication Rule first — only include it if it survives the filter:

- ✅ Happy path — include if it demonstrates real end-to-end/business flow, not pure logic
- ❌ Negative scenarios — include only for failure modes with system-level consequence
- ⚠️ Validation errors — include only if validation crosses a boundary (e.g. API contract), not internal-only
- 🔐 Permission scenarios (if applicable) — always include, rarely fully unit-tested
- 🚩 Feature flag ON state — always include if a flag is introduced or changed
- 🚩 Feature flag OFF state — always include if a flag is introduced or changed
- 🔄 Regression scenarios — include for HIGH/CRITICAL risk areas identified so far
- 🌍 Environment-specific behaviour (if applicable) — include if behaviour genuinely differs per environment

If a category is deliberately omitted because it is fully covered elsewhere, state this explicitly in the output (see below).

---

## Quality Criteria

Each scenario must be:
- **Clear** — unambiguous preconditions and expected results
- **Reproducible** — can be run by anyone with access to the environment
- **Deterministic** — the same input always produces the same output
- **Non-redundant** — justifies its existence against the Deduplication Rule above

---

## Required Output Note — Coverage Decisions

Alongside the scenarios, include a short **"Scenarios Not Written"** list: requirement IDs
(`FR`/`NFR`) or categories deliberately skipped because they are already covered by passing unit
tests, with a one-line justification each. This makes the deduplication decision visible and
reviewable.

Each written scenario should also state which requirement ID(s) it covers (e.g. "Covers: FR2, FR4")
so coverage stays traceable end to end.

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

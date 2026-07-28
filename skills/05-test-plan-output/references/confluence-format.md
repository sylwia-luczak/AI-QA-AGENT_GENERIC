# Confluence Page Formatting — Manual Test Scenarios

The Confluence page must contain **only manual test scenarios and their execution results**.
No analysis summaries, requirement breakdowns, risk descriptions, or other content from the
local test plan document.

---

## Scenario Header

Every scenario uses an **H3 heading** formatted as:
```
Test Scenario 01 — <Scenario Title>
```

- The heading text must be coloured **blue** (Confluence colour: `rgb(0,82,204)`)
- Number is always zero-padded and sequential: `01`, `02`, `03`, …
- Title is taken directly from the BDD scenario name

---

## Steps Format

Steps are written in **GIVEN / WHEN / THEN** format:

- The words **GIVEN**, **WHEN**, **THEN** (and **AND**) are always **bold**
- Step text is plain (no colour styling)
- Each step is on its own line
- After each step, include an **empty line** as a placeholder for a screenshot or evidence

```
**GIVEN** <precondition>

**WHEN** <action>

**THEN** <expected result>

**AND** <additional assertion>

```

---

## Verification Snippets

If a step requires verification via CLI, SQL, or an API call, include the relevant code snippet
directly after the relevant THEN/AND step, inside a Confluence `code` block.

---

## Results Section

After the last step of each scenario, include only:

```
*Result:*
*Status:* PASS / FAIL / BLOCKED
*Notes:*
```

No other content after the results block.

---

## What Must NOT Appear on the Confluence Page

- Requirements breakdowns
- Risk assessments
- Automation recommendations
- Regression matrices
- Open questions
- Any narrative text not part of a test step or result

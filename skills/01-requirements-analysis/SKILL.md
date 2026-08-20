---
name: 01-requirements-analysis
description: >
  Step 1 & 2 — Requirements Analysis and Implementation Verification.
  Use after receiving a JIRA ticket number and description. Extracts and structures functional
  requirements, non-functional requirements, edge cases, feature flags, integration points,
  and risk areas. Then verifies whether the implementation on the target branch matches the
  ticket requirements and reports any discrepancies.
  Can be used independently — requires only ticket context (number + description).
  Keywords: requirements, functional requirements, implementation check, branch verification,
  feature flags, ticket analysis, acceptance criteria, non-functional requirements.
argument-hint: '<PROJECT_KEY>-<TICKET_NUMBER> [branch name]'
---

# Step 01: Requirements Analysis + Implementation Verification

## Dependency
**Independent** — requires only a ticket number (or ticket context from the current session).
If no prior steps have been completed, fetch the ticket details:
```bash
python <SCRIPTS_DIR>/tools/jira_tool.py fetch <TICKET_NUMBER>
```

---

## Step 1 — Requirements Analysis

Extract and clearly structure the following from the ticket description. Assign each individual
requirement a stable ID — `FR1`, `FR2`, … for functional requirements and `NFR1`, `NFR2`, … for
non-functional requirements. Reuse these exact IDs unchanged in every later step (unit test
assessment, manual scenarios, test plan requirements breakdown) so coverage can be traced end
to end.

### Functional Requirements
- Core behaviours
- Business rules
- Validation logic

### Non-Functional Requirements
- Performance expectations
- Security requirements
- Logging requirements
- Environment-specific behaviour

### Additional Analysis
- Edge cases
- Feature flags (if any)
- Environmental dependencies
- Integration points (APIs, databases, external services)
- Risk areas
- Ambiguities
- Missing information
- Potential implementation risks

---

## Step 2 — Implementation Verification on Target Branch

Check the codebase on the specified branch and verify:

- Whether the implementation is present on the branch
- Whether implementation fully reflects ticket requirements
- Whether any required behaviour is missing
- Whether logic deviates from the described scope
- Whether feature flags are correctly integrated
- Whether environment-based logic is respected

**Clearly report any discrepancies found.**

If implementation is not yet on the target branch, note this and proceed with analysis based on
ticket description only.

---

## Output

1. **Structured requirements list** — functional, non-functional, edge cases, feature flags
2. **Implementation verification report** — matches / discrepancies / missing behaviour
3. **Risk areas** — ambiguities, missing ACs, potential issues

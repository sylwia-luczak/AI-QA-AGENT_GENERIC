---
name: ftrs-requirements-analysis
description: >
  FTRS Step 1 & 2 — Requirements Analysis and Implementation Verification.
  Use after receiving a JIRA ticket number and description in the FTRS project.
  Extracts and structures functional requirements, non-functional requirements, edge cases,
  feature flags, integration points, and risk areas. Then verifies whether the implementation
  on main branch matches the ticket requirements and reports any discrepancies.
  Keywords: requirements, functional requirements, implementation check, main branch verification,
  feature flags, FTRS ticket analysis.
mode: agent
---

# FTRS — Step 1️⃣ & 2️⃣: Requirements Analysis + Implementation Verification

---

## 1️⃣ Requirements Analysis

Extract and clearly structure the following from the ticket description:

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
- Integration points (APIs, DB, external services)
- Risk areas
- Ambiguities
- Missing information
- Potential implementation risks

---

## 2️⃣ Verification of Implementation on `main`

Check the codebase on the `main` branch and verify:

- Whether the implementation is merged into `main`
- Whether implementation fully reflects ticket requirements
- Whether any required behaviour is missing
- Whether logic deviates from the described scope
- Whether feature flags are correctly integrated
- Whether environment-based logic is respected

**Clearly report any discrepancies found.**

If implementation is not yet on `main`, note this and proceed with analysis based on ticket description only.

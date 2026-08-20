---
name: 05-regression-matrix
description: >
  Regression Risk Matrix — generates a structured risk assessment matrix for a JIRA ticket.
  Evaluates risk level (LOW/MEDIUM/HIGH/CRITICAL) across 13 system areas: API Behaviour,
  Existing Endpoints, Feature Flags, Caching, Authentication/Authorisation, API Gateway,
  Backend Logic, Database Layer, Data Integrity, Logging/Monitoring, Environment Configuration,
  CI/CD Pipeline, Backward Compatibility.
  For HIGH/CRITICAL risks, proposes targeted regression scenarios and automation reinforcement.
  Fully independent — can be used at any point in the workflow without prior steps.
  Must be included in every test plan document.
  Keywords: regression risk, risk matrix, impact assessment, production risk, feature flag risk,
  database risk, regression testing, risk assessment, system impact.
argument-hint: '<PROJECT_KEY>-<TICKET_NUMBER>'
---

# Step 05: Regression Risk Matrix

## Dependency
**Fully independent** — can be invoked at any point in the workflow with only ticket context.
If ticket details are not already available in this session, fetch them:
```bash
python <SCRIPTS_DIR>/tools/jira_tool.py fetch <TICKET_NUMBER>
```

---

## Purpose

The Regression Risk Matrix ensures that system-wide impact is evaluated beyond the immediate
scope of the ticket. It forces systemic thinking and prevents purely local validation.

This section is **mandatory** in every test plan document.

---

## Risk Levels

| Level | Meaning |
|---|---|
| **LOW** | Minimal impact, existing tests sufficient |
| **MEDIUM** | Some impact, targeted testing recommended |
| **HIGH** | Significant impact, regression testing required |
| **CRITICAL** | Could break core functionality, immediate attention needed |

---

## Risk Matrix

Complete the following table for every ticket:

| Area | Risk Level | Why? | Regression Needed? | Automation Update Needed? |
|---|---|---|---|---|
| API Behaviour | | | | |
| Existing Endpoints | | | | |
| Feature Flags | | | | |
| Caching | | | | |
| Authentication / Authorisation | | | | |
| API Gateway | | | | |
| Backend Logic | | | | |
| Database Layer | | | | |
| Data Integrity | | | | |
| Logging / Monitoring | | | | |
| Environment Configuration | | | | |
| CI/CD Pipeline | | | | |
| Backward Compatibility | | | | |

---

## Mandatory Analysis Rules

- Never mark all categories as LOW without justification
- Escalate risk if feature flags modify runtime behaviour
- Escalate risk if logic is environment-dependent
- Escalate risk if caching or async behaviour is involved
- Escalate risk if database schema or persistence logic is modified
- Escalate risk if endpoint-level gating is introduced
- Escalate risk if authentication or authorisation flow changes

---

## High / Critical Risk Handling

If any category is marked **HIGH** or **CRITICAL**, additionally:

1. Propose targeted regression scenarios for that area
2. Recommend automation reinforcement
3. Highlight potential production impact
4. Suggest rollout validation strategy (if applicable)

---

## Example Entry

| Area | Risk Level | Why? | Regression Needed? | Automation Update Needed? |
|---|---|---|---|---|
| Feature Flags | HIGH | Runtime behaviour changes without redeploy | Yes | Yes |
| Database Layer | MEDIUM | New write path added, existing reads unchanged | Yes | No |
| Backward Compatibility | LOW | Internal change only, no public contract change | No | No |

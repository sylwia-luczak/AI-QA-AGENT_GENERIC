---
name: ftrs-regression-matrix
description: >
  FTRS Regression Risk Matrix — generates a structured risk assessment matrix for a FTRS JIRA ticket.
  Evaluates risk level (LOW/MEDIUM/HIGH/CRITICAL) across 13 system areas: API Behavior, Existing Endpoints,
  Feature Flags, Caching, Authentication/Authorization, API Gateway, Lambda Logic, Database Layer,
  Data Integrity, Logging/Monitoring, Environment Configuration, CI/CD Pipeline, Backward Compatibility.
  For HIGH/CRITICAL risks, proposes targeted regression scenarios and automation reinforcement.
  Must be included in every test plan document. Keywords: regression risk, risk matrix, impact assessment,
  FTRS regression, production risk, feature flag risk, database risk.
mode: agent
---

# FTRS — Regression Risk Matrix

Generate a Regression Risk Matrix for this ticket. This section is **mandatory** in every test plan.

---

## 🎯 Purpose

The Regression Risk Matrix ensures that system-wide impact is evaluated beyond the scope of the ticket.

It forces systemic thinking and prevents local-only validation.

---

## 📋 Risk Levels

For each category, classify risk as:

| Level | Meaning |
|---|---|
| **LOW** | Minimal impact, existing tests sufficient |
| **MEDIUM** | Some impact, targeted testing recommended |
| **HIGH** | Significant impact, regression testing required |
| **CRITICAL** | Could break core functionality, immediate attention needed |

---

## 🔎 Risk Matrix

Complete the following table for every ticket:

| Area | Risk Level | Why? | Regression Needed? | Automation Update Needed? |
|---|---|---|---|---|
| API Behaviour | | | | |
| Existing Endpoints | | | | |
| Feature Flags | | | | |
| Caching | | | | |
| Authentication / Authorisation | | | | |
| API Gateway | | | | |
| Lambda Logic | | | | |
| Database Layer | | | | |
| Data Integrity | | | | |
| Logging / Monitoring | | | | |
| Environment Configuration | | | | |
| CI/CD Pipeline | | | | |
| Backward Compatibility | | | | |

---

## 🧠 Mandatory Analysis Rules

- Never mark all categories as LOW without justification
- Escalate risk if feature flags modify runtime behaviour
- Escalate risk if logic is environment-dependent
- Escalate risk if caching or async behaviour is involved
- Escalate risk if database schema or persistence logic is modified
- Escalate risk if endpoint-level gating is introduced
- Escalate risk if authentication flow changes

---

## 🚨 High / Critical Risk Handling

If any category is marked **HIGH** or **CRITICAL**, additionally:

1. Propose targeted regression scenarios
2. Recommend automation reinforcement
3. Highlight production impact
4. Suggest rollout validation strategy (if applicable)

---

## Example Entry

| Area | Risk Level | Why? | Regression Needed? | Automation Update Needed? |
|---|---|---|---|---|
| Feature Flags | HIGH | Runtime behaviour changes without redeploy | Yes | Yes |

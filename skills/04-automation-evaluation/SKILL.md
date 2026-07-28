---
name: 04-automation-evaluation
description: >
  Step 4 — Integration and Automation Test Evaluation. Evaluates whether automated integration
  tests should be added for a JIRA ticket. Considers cross-service impact, API changes, backend
  logic, database side effects, feature flags, caching, auth, logging, and CI impact.
  If automation is justified, proposes test scope, structure, mocking strategy, and example
  Gherkin automation scenarios.
  Can be used independently — requires only ticket context.
  Soft dependency on steps 01 and 03 (uses requirements and manual scenarios; will derive from
  ticket context if prior steps are not available in the session).
  Keywords: automation tests, integration tests, Playwright, Gherkin, BDD automation, CI impact,
  feature flag automation, automation evaluation, integration testing, test automation strategy.
argument-hint: '<PROJECT_KEY>-<TICKET_NUMBER>'
---

# Step 04: Integration / Automation Test Evaluation

## Dependency
**Soft dependency on steps 01 and 03.** Uses structured requirements and manual scenarios to
inform automation scope. If prior steps are not available in this session, fetch ticket context:
```bash
python <SCRIPTS_DIR>/tools/jira_tool.py fetch <TICKET_NUMBER>
```

---

## Evaluation Criteria

Consider each of the following and answer explicitly:

| Factor | Question |
|---|---|
| Cross-service impact | Does this change affect multiple services or components? |
| API changes | Are API routes, contracts, or gateway config affected? |
| Backend logic | Is core backend/processing logic changed? |
| Database side effects | Are database reads/writes affected? |
| Feature flags | Is behaviour gated behind a flag? |
| Caching behaviour | Could cached values cause stale or incorrect behaviour? |
| Authentication / authorisation | Are auth rules or permissions changed? |
| Logging validation | Should log output be validated as part of the change? |
| Environment-based config | Does behaviour differ across environments? |

---

## If Automation Is Justified

Propose the following:

- **Test scope** — what is being tested end-to-end
- **Test structure** — file and folder layout for new tests
- **Mocking strategy** — what is mocked vs real
- **Environment strategy** — which environment, test data approach
- **CI impact** — will new tests affect pipeline duration or stability?

---

## Technology Stack

Adapt the following to your project's actual technology stack:

- **Language**: Python (or your project's language)
- **UI testing**: Playwright (if applicable)
- **Test format**: Gherkin / BDD
- **Infrastructure**: Adapt to your cloud provider and services
  (e.g., AWS Lambda, DynamoDB; Azure Functions, CosmosDB; GCP Cloud Functions, Firestore)
- **Database access**: Adapt to your database tooling

---

## Example Automation Scenario

**Tags:** `@integration` `@data-processing`
**Feature:** Data Processing Pipeline

```gherkin
Background:
  Given the test environment is configured
  And the source system has test data
  And the target system is ready to receive records

Scenario: Happy path — record is processed and created correctly
  Given a "<entity_type>" record exists in the source system with attributes
    | key    | value            |
    | id     | <test_id>        |
    | type   | <entity_type>    |
    | name   | Test Entity Name |
    | status | active           |

  When the processing pipeline is triggered for record "<test_id>"

  Then the event metrics should be:
    - 1 total, 1 processed, 0 errors

  And the target system contains the correct record
  And the audit log confirms successful processing
```

---

## Naming Convention for Test Data

- Use a consistent prefix or pattern linking test data to the ticket number
- Use natural, realistic names — avoid excessive use of "TEST" in display values
- Document the naming convention so any team member can reproduce the data

---

## If Automation Is NOT Justified

State clearly why automation is not warranted and confirm that manual testing is sufficient.

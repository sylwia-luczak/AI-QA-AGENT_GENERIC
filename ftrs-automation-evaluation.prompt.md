---
name: ftrs-automation-evaluation
description: >
  FTRS Step 5 — Integration and Automation Test Evaluation. Use after the manual test plan step
  for a FTRS JIRA ticket. Evaluates whether automated integration tests should be added, considering
  cross-service impact, API Gateway, Lambda, DynamoDB, feature flags, caching, auth, logging,
  and CI impact. If automation is justified, proposes test scope, structure, mocking strategy,
  and example Gherkin automation scenarios using Python, Playwright, Gherkin BDD, AWS.
  Keywords: automation tests, integration tests, Playwright, Gherkin, BDD automation, CI impact,
  Lambda testing, DynamoDB, feature flag automation, FTRS automation.
mode: agent
---

# FTRS — Step 5️⃣: Integration / Automation Test Evaluation

Evaluate whether integration or automated tests should be added for this ticket.

---

## Evaluation Criteria

Consider each of the following (answer explicitly):

| Factor | Question |
|---|---|
| Cross-service impact | Does this change affect multiple services? |
| API Gateway | Are API routes or gateway config affected? |
| Lambda behaviour | Is Lambda logic changed? |
| Database side effects | Are DynamoDB writes/reads affected? |
| Feature flags | Is behaviour gated behind a flag? |
| Caching behaviour | Could cached values cause stale behaviour? |
| Authentication / authorisation | Are auth rules changed? |
| Logging validation | Should CloudWatch output be validated? |
| Environment-based config | Does behaviour differ across environments? |

---

## If Automation Is Justified

### Propose:
- **Test scope** — what is being tested end-to-end
- **Test structure** — file/folder layout
- **Mocking strategy** — what is mocked vs real
- **Environment strategy** — which environment, test data approach
- **CI impact** — will new tests affect pipeline duration or stability?

---

## Technology Stack

- **Language**: Python
- **UI testing**: Playwright
- **Test format**: Gherkin (BDD)
- **Infrastructure**: AWS — DynamoDB, Athena, Lambda, CloudWatch, SQS
- **Database access**: DBeaver and SQL (Old DOS)

---

## Naming Convention for Test Data (OldDOS Services)

- **GP Practice IDs**: `9XXXX0Y` — where `XXXX` = ticket number, `Y` = scenario number
- **Pharmacy IDs**: `8XXXX0Y` — where `XXXX` = ticket number, `Y` = scenario number
- Names should be natural — avoid ticket numbers in names and excessive use of "TEST"

---

## Example Automation Scenario

**Tags:** `@data-migration`
**Feature:** Data Migration

```gherkin
Background:
  Given the test environment is configured
  And the DoS database has test data
  And DynamoDB tables are ready

Scenario: Happy path migration for a GP Practice
  Given a "Service" exists in DoS with attributes
    | key        | value                     |
    | id         | 10005752                  |
    | uid        | 138179                    |
    | name       | Abbey Medical Practice    |
    | odscode    | M81094                    |
    | typeid     | 100                       |
    | statusid   | 1                         |

  When the data migration process is run for table 'services', ID '10005752' and method 'insert'

  Then the SQS event metrics should be:
    - 1 total, 1 supported, 0 unsupported
    - 1 transformed, 1 inserted, 0 updated
    - 0 skipped, 0 errors

  And there is 1 organisation, 1 location and 1 healthcare service created
  And the state table contains a record for key 'services#10005752' with version 1
```

---

## If Automation Is NOT Justified

State clearly why automation is not warranted and confirm that manual testing is sufficient.

# Data handling & security (current state)

*Practical checklist, not a legal opinion. Have counsel review the client contract and data-processing terms.*

## What the product does today
- Reads client data in memory for the session; **raw rows are never written to disk or to the database**
  (a test enforces this). Stored: assumptions, run totals, report fingerprints, column mappings, human decisions.
- Read-only on client systems: SQL is restricted to a single SELECT; REST is https-only with private addresses blocked.
- Named users with roles (viewer / reviewer / admin), PBKDF2 password hashes; no plain-text passwords in secrets.
- Every decision is written to a **hash-chained** audit trail; editing or deleting a row is detected on screen.
- The AI features receive only aggregates and top-contributor labels (no employee IDs, e-mails or payroll lines),
  and only if an API key is configured. The Copilot answers through calculation tools and flags figures it cannot
  trace to a tool result.
- Findings are exceptions for review, never grounds for a payroll or disciplinary action by themselves.

## Not done yet (be upfront with clients)
SSO / MFA, per-client tenant isolation in one deployment, encryption of the SQLite file at rest (use disk encryption),
independent penetration test, ISO 27001 / SOC 2.

## Before any pilot with real people-data
Agree in writing: purpose, fields supplied, retention and deletion, hosting region, a named contact for data
requests. Pseudonymise employee IDs where the client can. Use the container deployment in an India region, not the
public demo host.

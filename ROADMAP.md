# Roadmap

**Next 30 days (earn the first paid pilot)**
- Run two free audits on friendly companies' real exports; log measured recovery per rule.
- Harden data cleaning from what breaks in real files (merged cells, Excel serial dates, rupee formats).

**60-90 days (make it a subscription)**
- First vendor-specific connector for the most common client stack (decide from pilots; likely one HRIS + Tally/SAP export).
- Hosted single-tenant container per client in an India region; scheduled monitor; weekly e-mail digest to CFO.
- Industry rule packs (pharma batch-release delays, textile idle looms, logistics detention charges).

**6 months**
- Postgres store, SSO, per-client tenancy; ticketing hand-off (Jira / ServiceNow) after approval.
- Optional write-back for narrow, reversible actions (e.g. disable an orphaned SaaS licence) behind a second approver.
- Benchmarks from measured recoveries across clients.

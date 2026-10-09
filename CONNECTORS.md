# Connecting to client systems

Three ways in, from easiest to most automated. All are read-only.

## 1. Files (day-one pilots)
Upload CSV/Excel in any column layout on **0. Connect & Data**. The mapping screen pre-fills suggestions
(known header names, then fuzzy match). Confirm once, click *Remember*. Fields that are safe to leave empty
(e.g. overtime hours) default to empty; fields where emptiness would create false findings (e.g. gate-in time,
paid date) are **required**.

## 2. Read-only SQL (best for SAP / Tally / Dynamics / HRIS databases)
Ask the client's IT for a **read replica or reporting views** and a **read-only user**. Put credentials in
secrets/environment variables and reference them as `${NAME}`. Write one `SELECT` per dataset that aliases the
client's columns to ours (`SELECT emp_code AS employee_id, ...`). Anything that is not a single SELECT is refused.
Drivers: `psycopg2-binary` (Postgres), `pymysql`, `pyodbc` (SQL Server), `oracledb`, `hdbcli` (SAP HANA). Add the
driver to `requirements.txt`.

## 3. REST (cloud HRIS / ERP APIs)
Generic client: bearer / header-key / basic auth, retries, page / offset / cursor pagination, https-only,
private-network addresses refused. Fill `base_url`, `path`, `records_path` and `field_map` from the **vendor's own API
documentation**. This repo does not ship vendor-specific endpoints, because each tenant differs and a wrong guess is
worse than none. Treat the first connection to each vendor as a half-day integration task, then reuse the config.

## Dataset fields
| Dataset | Required fields |
|---|---|
| attendance | employee_id, date, shift, cell, paid_hours, hourly_rate, overtime_hours, gate_in |
| machine_log | date, shift, cell, scheduled_hours, active_hours, downtime_reason |
| milestones | milestone_id, project, client, value_inr, signoff_date, invoice_date |
| saas | user_email, app, monthly_cost_inr, last_login_date, employment_status |
| employees | employee_id, department, designation, ctc_inr, join_date, exit_date, last_rating, last_promotion_date |
| payroll | employee_id, pay_month, gross_inr |
| ap_invoices | invoice_id, vendor, invoice_no, invoice_date, amount_inr, paid_date |

Blank `invoice_date` = not yet invoiced. Blank `exit_date` = still employed. Dates in ISO (2026-09-30) or day-first (30/09/2026).

## Adding a new rule
Write `detect_xxx(data..., cfg) -> Finding` in `detectors.py`, add it to `DETECTORS`, give it a realisation
percentage in `DEFAULT_CONFIG`, add an action block in `agent.py`, and a test with a hand-computed expected figure
in `tests/test_engine.py`.

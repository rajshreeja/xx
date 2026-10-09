"""
Read-only SQL connector (SQLAlchemy). Works with Postgres, MySQL, SQL Server, Oracle and SAP HANA
as long as the matching driver is installed, e.g. psycopg2-binary, pymysql, pyodbc, oracledb, hdbcli.

Point it at a READ REPLICA or a reporting view with a read-only database user. As a second line
of defence, queries are checked here and anything that is not a single SELECT is refused.

Config:
{
  "kind": "sql",
  "url": "postgresql+psycopg2://${DB_USER}:${DB_PASS}@host:5432/erp",
  "max_rows": 2000000,
  "queries": { "attendance": "SELECT emp_code AS employee_id, ... FROM v_attendance WHERE att_date >= :since" },
  "params": { "since": "2026-06-01" }
}
"""
from __future__ import annotations

import re

import pandas as pd

from .base import Connector, expand_env

_FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|create|grant|revoke|truncate|merge|exec|execute|call|"
    r"into|replace|vacuum|attach|pragma)\b", re.I)


def assert_read_only(sql: str) -> str:
    s = sql.strip().rstrip(";").strip()
    if ";" in s:
        raise ValueError("Only a single statement is allowed.")
    if not re.match(r"^(select|with)\b", s, re.I):
        raise ValueError("Only SELECT queries are allowed.")
    # strip string literals before keyword check so 'update' inside text is not a false alarm
    scrubbed = re.sub(r"'(?:[^']|'')*'", "''", s)
    scrubbed = re.sub(r"--[^\n]*|/\*.*?\*/", " ", scrubbed, flags=re.S)
    m = _FORBIDDEN.search(scrubbed)
    if m:
        raise ValueError(f"Keyword '{m.group(0)}' is not allowed in a read-only query.")
    return s


class SQLConnector(Connector):
    kind = "sql"

    def _engine(self):
        from sqlalchemy import create_engine
        return create_engine(expand_env(self.config["url"]), pool_pre_ping=True)

    def datasets(self):
        return list(self.config.get("queries", {}))

    def fetch(self, dataset: str) -> pd.DataFrame:
        from sqlalchemy import text
        sql = assert_read_only(self.config["queries"][dataset])
        params = self.config.get("params", {})
        max_rows = int(self.config.get("max_rows", 2_000_000))
        eng = self._engine()
        try:
            with eng.connect() as c:
                df = pd.read_sql(text(sql), c, params=params)
        finally:
            eng.dispose()
        if len(df) > max_rows:
            raise ValueError(f"Query returned {len(df):,} rows, above the max_rows limit of {max_rows:,}.")
        return df

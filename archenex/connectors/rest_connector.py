"""
Generic JSON REST connector with auth, retries and pagination.

This is deliberately vendor-neutral. HRIS / ERP vendors each document their own endpoints; fill in
the path, auth style and record path from THEIR API documentation, then confirm with Test.

Config:
{
  "kind": "rest",
  "base_url": "https://api.example-hris.com",
  "auth": {"type": "bearer", "token": "${HRIS_TOKEN}"},        // or {"type":"header","name":"X-Api-Key","value":"${KEY}"}
                                                              // or {"type":"basic","user":"..","password":".."}
  "endpoints": {
     "attendance": {
        "path": "/v1/attendance", "params": {"from": "2026-06-01"},
        "records_path": "data.items",                          // dotted path to the list in the JSON
        "pagination": {"type": "page", "page_param": "page", "size_param": "per_page", "size": 500, "max_pages": 400},
        "field_map": {"emp_code": "employee_id"}               // optional renames
     }
  }
}
Pagination types: "page" (page=1,2,..), "offset" (offset+limit), "cursor" (next token at cursor_path).
"""
from __future__ import annotations

import ipaddress
import socket
import time
from urllib.parse import urlparse

import pandas as pd

from .base import Connector, expand_env


def _dig(obj, path: str):
    for part in [p for p in (path or "").split(".") if p]:
        obj = obj[part] if isinstance(obj, dict) else obj[int(part)]
    return obj


def check_url(url: str, allow_private: bool = False) -> None:
    u = urlparse(url)
    host = u.hostname or ""
    local = host in ("localhost", "127.0.0.1", "::1")
    if u.scheme != "https" and not (local and allow_private):
        raise ValueError("Only https:// endpoints are allowed.")
    if allow_private:
        return
    try:
        for fam, _, _, _, addr in socket.getaddrinfo(host, None):
            ip = ipaddress.ip_address(addr[0])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
                raise ValueError(f"Host {host} resolves to a private address; refused.")
    except socket.gaierror as e:
        raise ValueError(f"Cannot resolve host {host}: {e}")


class RESTConnector(Connector):
    kind = "rest"

    def datasets(self):
        return list(self.config.get("endpoints", {}))

    def _headers_auth(self):
        a = expand_env(self.config.get("auth", {}))
        headers, auth = {"Accept": "application/json"}, None
        t = a.get("type")
        if t == "bearer":
            headers["Authorization"] = f"Bearer {a['token']}"
        elif t == "header":
            headers[a["name"]] = a["value"]
        elif t == "basic":
            auth = (a["user"], a["password"])
        return headers, auth

    def _get(self, session, url, params, headers, auth, retries=3):
        import requests
        for i in range(retries):
            try:
                r = session.get(url, params=params, headers=headers, auth=auth, timeout=30)
                if r.status_code in (429, 500, 502, 503, 504) and i < retries - 1:
                    time.sleep(1.5 * (i + 1))
                    continue
                r.raise_for_status()
                return r.json()
            except requests.ConnectionError:
                if i == retries - 1:
                    raise
                time.sleep(1.5 * (i + 1))

    def fetch(self, dataset: str) -> pd.DataFrame:
        import requests
        ep = self.config["endpoints"][dataset]
        base = expand_env(self.config["base_url"]).rstrip("/")
        url = base + ep["path"]
        check_url(url, bool(self.config.get("allow_private", False)))
        headers, auth = self._headers_auth()
        params = dict(expand_env(ep.get("params", {})))
        pg = ep.get("pagination") or {}
        ptype = pg.get("type")
        max_pages = int(pg.get("max_pages", 500))
        rows: list = []
        with requests.Session() as s:
            page, offset, cursor = 1, 0, None
            for _ in range(max_pages):
                q = dict(params)
                if ptype == "page":
                    q[pg.get("page_param", "page")] = page
                    q[pg.get("size_param", "per_page")] = pg.get("size", 500)
                elif ptype == "offset":
                    q[pg.get("offset_param", "offset")] = offset
                    q[pg.get("limit_param", "limit")] = pg.get("size", 500)
                elif ptype == "cursor" and cursor:
                    q[pg.get("cursor_param", "cursor")] = cursor
                body = self._get(s, url, q, headers, auth)
                recs = _dig(body, ep.get("records_path", "")) if ep.get("records_path") else body
                if not isinstance(recs, list):
                    raise ValueError("records_path did not point to a list.")
                rows.extend(recs)
                if not ptype or not recs:
                    break
                if ptype == "page":
                    if len(recs) < int(pg.get("size", 500)):
                        break
                    page += 1
                elif ptype == "offset":
                    if len(recs) < int(pg.get("size", 500)):
                        break
                    offset += len(recs)
                elif ptype == "cursor":
                    cursor = _dig(body, pg.get("cursor_path", "next")) if pg.get("cursor_path", "next") else None
                    if not cursor:
                        break
        df = pd.json_normalize(rows) if rows else pd.DataFrame()
        fm = ep.get("field_map")
        return df.rename(columns=fm) if fm else df

"""Connector registry. build_connectors(json_config) -> {name: Connector}."""
from __future__ import annotations

import json

from .base import Connector, expand_env
from .file_connector import FileConnector, read_table
from .rest_connector import RESTConnector
from .sql_connector import SQLConnector, assert_read_only

KINDS = {"files": FileConnector, "sql": SQLConnector, "rest": RESTConnector}


def build_connectors(config: dict | str) -> dict[str, Connector]:
    if isinstance(config, str):
        config = json.loads(config)
    out = {}
    for name, c in (config.get("connections") or {}).items():
        kind = c.get("kind")
        if kind not in KINDS:
            raise ValueError(f"Connection '{name}': unknown kind '{kind}'. Use one of {sorted(KINDS)}.")
        out[name] = KINDS[kind](name, c)
    return out


__all__ = ["Connector", "FileConnector", "RESTConnector", "SQLConnector", "build_connectors",
           "read_table", "assert_read_only", "expand_env"]

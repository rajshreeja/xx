"""File connector: CSV / Excel bytes or paths. Used by uploads, the CLI and scheduled folder drops."""
from __future__ import annotations

import io
import os

import pandas as pd

from .base import Connector


def read_table(name: str, data: bytes | str) -> pd.DataFrame:
    low = name.lower()
    src = io.BytesIO(data) if isinstance(data, (bytes, bytearray)) else data
    if low.endswith((".xlsx", ".xlsm", ".xls")):
        return pd.read_excel(src)
    try:
        return pd.read_csv(src)
    except UnicodeDecodeError:
        if isinstance(src, io.BytesIO):
            src.seek(0)
        return pd.read_csv(src, encoding="latin-1")


class FileConnector(Connector):
    """Config: {"kind":"files","folder":"/data/acme","files":{"attendance":"attendance.csv", ...}}"""
    kind = "files"

    def datasets(self):
        return list(self.config.get("files", {}))

    def fetch(self, dataset: str) -> pd.DataFrame:
        path = os.path.join(self.config.get("folder", "."), self.config["files"][dataset])
        return read_table(path, path)

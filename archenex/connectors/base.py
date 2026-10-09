"""Connector interface. A connector READS a dataset from a client system. It never writes back."""
from __future__ import annotations

import abc
import os
import re

import pandas as pd

_ENV = re.compile(r"\$\{([A-Z0-9_]+)\}")


def expand_env(value):
    """Replace ${NAME} with the environment variable NAME so secrets never live in config files."""
    if isinstance(value, str):
        def rep(m):
            v = os.environ.get(m.group(1))
            if v is None:
                raise KeyError(f"Environment variable {m.group(1)} is not set")
            return v
        return _ENV.sub(rep, value)
    if isinstance(value, dict):
        return {k: expand_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [expand_env(v) for v in value]
    return value


class Connector(abc.ABC):
    kind = "base"

    def __init__(self, name: str, config: dict):
        self.name = name
        self.config = config

    @abc.abstractmethod
    def datasets(self) -> list[str]:
        """Dataset names this connector can supply."""

    @abc.abstractmethod
    def fetch(self, dataset: str) -> pd.DataFrame:
        """Return the raw frame for a dataset (column mapping is applied afterwards)."""

    def test(self) -> tuple[bool, str]:
        """Cheap health check used by the Connections screen."""
        try:
            ds = self.datasets()
            if not ds:
                return False, "No datasets configured."
            df = self.fetch(ds[0])
            return True, f"OK: read {len(df):,} rows from '{ds[0]}'."
        except Exception as e:  # surface the reason to the analyst
            return False, f"{type(e).__name__}: {e}"

"""Quarterly fundamental data provider module."""

from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

import pandas as pd


class DataProviderBase(ABC):
    """Interface for providing quarterly data."""

    @abstractmethod
    def get_data_for_quarter(self, quarter: str) -> pd.DataFrame:
        """Return a DataFrame for the given quarter (e.g., '2024Q1')."""
        ...


class CSVDataProvider(DataProviderBase):
    """Load quarterly fundamentals from a local CSV file."""

    def __init__(self, file_path: Union[str, Path]) -> None:
        self._file_path: Path = Path(file_path)
        try:
            self._data: pd.DataFrame = pd.read_csv(self._file_path)
        except Exception:
            self._data = pd.DataFrame()

    def get_data_for_quarter(self, quarter: str) -> pd.DataFrame:
        """Return rows where the 'quarter' column equals the requested period."""
        df = self._data
        if "quarter" not in df.columns:
            return pd.DataFrame()

        filtered = df[df["quarter"] == quarter]
        return filtered.reset_index(drop=True)
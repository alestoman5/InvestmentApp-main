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

    @abstractmethod
    def available_years(self) -> list[int]:
        """Return the sorted years for which data exists."""
        ...


class CSVDataProvider(DataProviderBase):
    """Load quarterly fundamentals from a local CSV file."""

    #: Where users can obtain the fundamentals dataset.
    DATA_SOURCE_URL = (
        "https://www.kaggle.com/code/vladosht/s-p-500-fundamental-data-model"
    )

    def __init__(self, file_path: Union[str, Path]) -> None:
        self._file_path: Path = Path(file_path)
        # Surface a missing file as a real, actionable error rather than as an
        # empty screen result that looks like "no stocks met criteria".
        try:
            self._data: pd.DataFrame = pd.read_csv(self._file_path)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Fundamentals dataset not found at {self._file_path}.\n"
                f"This file is not bundled with the repository. Generate it "
                f"from {self.DATA_SOURCE_URL} and save it to that path.\n"
                f"See the 'Data' section of README.md for details."
            ) from None

    def available_years(self) -> list[int]:
        """Return the sorted years covered by the 'quarter' column ('2009Q1')."""
        if "quarter" not in self._data.columns:
            return []
        years = pd.to_numeric(
            self._data["quarter"].astype(str).str.slice(0, 4), errors="coerce"
        ).dropna()
        return sorted({int(y) for y in years})

    def get_data_for_quarter(self, quarter: str) -> pd.DataFrame:
        """Return rows where the 'quarter' column equals the requested period."""
        df = self._data
        if "quarter" not in df.columns:
            return pd.DataFrame()

        filtered = df[df["quarter"] == quarter]
        return filtered.reset_index(drop=True)

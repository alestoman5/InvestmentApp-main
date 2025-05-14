"""Stock screener module."""

from __future__ import annotations

from typing import Mapping, Protocol

import pandas as pd


class DataProvider(Protocol):
    def get_data_for_quarter(self, period: str) -> pd.DataFrame | None:
        ...


class StockScreener:
    """Filter tickers by quarter and metric criteria."""

    def __init__(self, data_provider: DataProvider) -> None:
        self._data_provider = data_provider

    def filter_stocks(
        self,
        year: int,
        quarter: str,
        criteria: Mapping[str, tuple[str, float]],
    ) -> list[str]:
        """Return tickers matching all filters."""
        quarter = f"{year}{quarter}"
        df = self._data_provider.get_data_for_quarter(quarter)
        if df is None or df.empty:
            return [] #AT raise error

        for metric, (condition, threshold) in criteria.items():
            if metric not in df.columns:
                continue #AT - přidat raise 
            if condition == "Over":
                df = df[df[metric] > threshold]
            else:
                df = df[df[metric] < threshold]

        return df.get("ticker", []).tolist()
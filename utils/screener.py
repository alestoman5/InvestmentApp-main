"""Stock screener module."""

from __future__ import annotations
from typing import Mapping

from utils.data_provider import DataProviderBase as DataProvider


class StockScreener:
    """Filter tickers by quarter and metric criteria."""

    def __init__(self, data_provider: DataProvider) -> None:
        self.data_provider = data_provider

    def available_years(self) -> list[int]:
        """Return the years the underlying data source covers."""
        return self.data_provider.available_years()

    def filter_stocks(
        self,
        year: int,
        quarter: str,
        criteria: Mapping[str, tuple[str, float]],
    ) -> list[str]:
        """Return tickers matching all filters."""
        quarter = f"{year}{quarter}"
        df = self.data_provider.get_data_for_quarter(quarter)
        if df is None or df.empty:
            return []
        if "ticker" not in df.columns:
            raise ValueError("Data source has no 'ticker' column.")

        for metric, (condition, value) in criteria.items():
            if metric not in df.columns:
                raise ValueError(f"Metric '{metric}' not found in data columns.")
            if condition == "Over":
                df = df[df[metric] > value]
            else:
                df = df[df[metric] < value]

        return df["ticker"].tolist()

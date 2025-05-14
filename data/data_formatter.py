"""Format raw data into Close price series."""

from __future__ import annotations
from typing import Sequence, Dict

import pandas as pd


class DataFormatter:
    """Convert raw yfinance output to ticker-close Series mapping."""

    @staticmethod
    def format_data(
        raw: pd.DataFrame, tickers: Sequence[str]
    ) -> Dict[str, pd.Series]:
        """Return dict of closing price Series for each ticker."""
        formatted: Dict[str, pd.Series] = {}
        for ticker in tickers:
            try:
                if len(tickers) == 1:
                    series = raw['Close']
                else:
                    series = raw[ticker]['Close']
            except (KeyError, TypeError):
                continue
            formatted[ticker] = series
        return formatted
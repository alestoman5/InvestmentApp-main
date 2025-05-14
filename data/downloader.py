"""Download historical data via yfinance."""

from __future__ import annotations
from datetime import date
from typing import Sequence, Union

import pandas as pd
import yfinance as yf


class Downloader:
    """Fetch historical price data for given tickers and period."""

    @staticmethod
    def download(
        tickers: Sequence[str],
        start_date: Union[str, date],
        end_date: Union[str, date],
    ) -> pd.DataFrame:
        """Return raw price data DataFrame or empty DataFrame on failure."""
        try:
            return yf.download(
                tickers=tickers,
                start=start_date,
                end=end_date,
                group_by="ticker",
                threads=True,
                progress=True,
            )
        except Exception:
            return pd.DataFrame()
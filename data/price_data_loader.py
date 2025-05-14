"""Load historical 'Close' price data with caching."""

from __future__ import annotations
from datetime import date
from typing import Sequence, Union, Tuple, Dict

import pandas as pd

from data.downloader import Downloader
from data.data_formatter import DataFormatter


class Cache:
    """In-memory cache for price series."""
    _price_cache: Dict[Tuple[str, str, str], pd.Series] = {}


class PriceDataLoader:
    """Retrieve historical 'Close' prices, using cache when available."""

    @classmethod
    def load(
        cls,
        tickers: Sequence[str],
        start_date: Union[str, date],
        end_date: Union[str, date],
    ) -> pd.DataFrame:
        """
        Load 'Close' price data for specified tickers and date range.
        Caches results to avoid redundant downloads.
        """
        if not tickers:
            return pd.DataFrame()

        start_key = str(start_date)
        end_key = str(end_date)

        missing = [
            ticker
            for ticker in tickers
            if (ticker, start_key, end_key) not in Cache._price_cache
        ]

        if missing:
            raw_data = Downloader.download(missing, start_date, end_date)
            formatted_data = DataFormatter.format_data(raw_data, missing)
            for ticker, series in formatted_data.items():
                if not series.empty:
                    Cache._price_cache[(ticker, start_key, end_key)] = series

        data: Dict[str, pd.Series] = {
            ticker: Cache._price_cache[(ticker, start_key, end_key)]
            for ticker in tickers
            if (ticker, start_key, end_key) in Cache._price_cache
        }

        return pd.DataFrame(data).dropna(axis=1, how="all")

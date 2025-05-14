"""Fetch price data using the PriceDataLoader."""

from __future__ import annotations
from datetime import date
from typing import Sequence, Union

import pandas as pd

from data.price_data_loader import PriceDataLoader


class DataFetcher:
    """Retrieve historical price data for given tickers."""

    @staticmethod
    def fetch_data(
        tickers: Sequence[str],
        start_date: Union[str, date],
        end_date: Union[str, date],
    ) -> pd.DataFrame:
        """Return price DataFrame for specified tickers and date range."""
        return PriceDataLoader.load(tickers, start_date, end_date)
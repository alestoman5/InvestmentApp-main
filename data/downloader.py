"""Download historical data via yfinance."""

from __future__ import annotations
from datetime import date
from typing import Sequence, Union

import yfinance as yf


class Downloader:
    """Fetch historical price data for given tickers and period."""

    @staticmethod
    def download(
        tickers: Sequence[str],
        start_date: Union[str, date],
        end_date: Union[str, date],
    ) -> pd.DataFrame:
        """Return the raw yfinance price DataFrame.

        Raises RuntimeError if the download fails, so the caller can surface
        the reason instead of showing an empty result.
        """
        try:
            return yf.download(
                tickers=tickers,
                start=start_date,
                end=end_date,
                group_by="ticker",
                threads=True,
                progress=False,
            )
        except Exception as exc:
            raise RuntimeError(f"Failed to download price data: {exc}") from exc

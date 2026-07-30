"""Abstract base class for investment strategies."""

from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date
from typing import Sequence, Optional, Union

import pandas as pd
from matplotlib.figure import Figure

from strategies.data_fetcher import DataFetcher
from strategies.stats_calculator import StatsCalculator, StatsData
from strategies.visualizer import Visualizer


class StrategyBase(ABC):
    """Base class for investment strategies.

    Handles data fetching, simulation, statistics, and visualization.
    """

    def __init__(
        self,
        tickers: Sequence[str],
        start_date: Union[date, str],
        end_date: Union[date, str],
    ) -> None:
        self._tickers: list[str] = list(tickers)
        self._start_date: Union[date, str] = start_date
        self._end_date: Union[date, str] = end_date

        # Fetch price data for the given period
        self._price_data: pd.DataFrame = DataFetcher.fetch_data(
            self._tickers, self._start_date, self._end_date
        )
        self.portfolio_series: Optional[pd.Series] = None

        self.simulate()

    @abstractmethod
    def simulate(self) -> None:
        """Run strategy simulation and populate `self.portfolio_series`."""
        ...

    def get_statistics(self) -> Optional[StatsData]:
        """Calculate and return performance metrics: total return, CAGR, volatility,
        max drawdown, Sharpe ratio, and win rate."""
        return StatsCalculator.calculate(self.portfolio_series)

    def plot(self, parent_frame: Optional[object] = None) -> Figure:
        """Return a Matplotlib figure of portfolio performance."""
        return Visualizer.plot(self.portfolio_series, parent_frame)

"""Concrete periodic rebalance strategy implementation."""

from __future__ import annotations

import pandas as pd

from .strategy_abstract import StrategyBase
from .registry import register_strategy

@register_strategy("Periodic Rebalance")
class PeriodicRebalanceStrategy(StrategyBase):
    """Rebalance to equal weights each day."""

    def simulate(self) -> None:
        """Populate portfolio_series with daily returns."""
        cols = [t for t in self._tickers if t in self._price_data.columns]
        prices = self._price_data[cols].dropna(axis=1, how="all").ffill()
        if prices.empty:
            self.portfolio_series = pd.Series(dtype=float)
            return

        # mean() skips NaN, so tickers without a price yet are excluded from
        # that day's average rather than counted as a 0% return.
        daily_returns = prices.pct_change()
        port_returns = daily_returns.mean(axis=1).fillna(0)
        self.portfolio_series = (1 + port_returns).cumprod()

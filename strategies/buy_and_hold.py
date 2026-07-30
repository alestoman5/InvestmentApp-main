"""Concrete buy-and-hold strategy implementation."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .strategy_abstract import StrategyBase
from .registry import register_strategy

@register_strategy("Buy and Hold")
class BuyAndHoldStrategy(StrategyBase):
    """Buy once at start date and hold."""

    def simulate(self) -> None:
        """Populate portfolio_series with normalized prices."""
        cols = [t for t in self._tickers if t in self._price_data.columns]
        prices = self._price_data[cols].dropna(axis=1, how="all").ffill()
        # A ticker with no price on the first day would normalize to all-NaN
        # and poison the portfolio average, so drop it.
        prices = prices.loc[:, prices.iloc[0].notna()] if not prices.empty else prices
        if prices.empty:
            self.portfolio_series = pd.Series(dtype=float)
            return

        norm = prices / prices.iloc[0]
        weights = np.full(len(norm.columns), 1 / len(norm.columns))
        self.portfolio_series = norm.dot(weights)

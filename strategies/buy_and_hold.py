"""Concrete buy-and-hold strategy implementation."""

from __future__ import annotations

from datetime import date
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
        prices = self._price_data[cols].dropna(axis=1, how="all")
        if prices.empty:
            self.portfolio_series = pd.Series(dtype=float)
            return

        norm = prices / prices.iloc[0]
        weights = np.full(len(norm.columns), 1 / len(norm.columns))
        self.portfolio_series = norm.dot(weights)

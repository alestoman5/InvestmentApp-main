"""Compute portfolio performance metrics."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

import pandas as pd


@dataclass(frozen=True)
class StatsData:
    total_return: float
    annualized_return: float
    volatility: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float


class StatsCalculator:
    """Calculate key portfolio stats."""

    @staticmethod
    def calculate(
        series: Optional[pd.Series]
    ) -> Optional[StatsData]:
        """Return performance metrics or None if no data."""
        if series is None or series.empty:
            return None

        initial_value = series.iloc[0]
        final_value = series.iloc[-1]
        total_return = (final_value / initial_value - 1) * 100

        days = (series.index[-1] - series.index[0]).days
        years = days / 365.25 if days > 0 else 0
        annualized_return = (
            (final_value / initial_value) ** (1 / years) * 100 - 100
            if years > 0 else 0.0
        )

        returns = series.pct_change().dropna()
        volatility = (
            returns.std() * (252 ** 0.5) * 100
            if not returns.empty else 0.0
        )

        drawdowns = (series / series.cummax() - 1) * 100
        max_drawdown = drawdowns.min()

        # Annualized excess return over annualized volatility.
        risk_free_rate = 0.02
        sharpe_ratio = (
            ((annualized_return / 100 - risk_free_rate) /
             (volatility / 100))
            if volatility > 0 else 0.0
        )

        monthly = series.resample("ME").last().pct_change().dropna()
        win_rate = (
            monthly.gt(0).sum() / len(monthly) * 100
            if not monthly.empty else 0.0
        )

        # Round all metrics and construct dataclass
        rounded = tuple(round(x, 2) for x in (
            total_return,
            annualized_return,
            volatility,
            max_drawdown,
            sharpe_ratio,
            win_rate,
        ))
        return StatsData(*rounded)

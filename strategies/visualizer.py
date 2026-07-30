"""Plot normalized portfolio time series."""

from __future__ import annotations
from typing import Optional

import pandas as pd
from matplotlib.figure import Figure

from utils.config import GRAPH_COLOR


class Visualizer:
    @staticmethod
    def plot(
        series: pd.Series,
        parent_frame: Optional[object] = None,
    ) -> Figure:
        """Plot normalized portfolio values over time."""
        if series.empty:
            raise ValueError("Portfolio series is empty.")

        # Build the Figure directly rather than via pyplot: a pyplot figure
        # stays registered globally and leaks on every backtest run.
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.plot(series, label="Equally Weighted Portfolio", color=GRAPH_COLOR)
        ax.set_title("Portfolio Performance")
        ax.set_xlabel("Date")
        ax.set_ylabel("Normalized Value")
        ax.grid(which="both", linestyle="--", linewidth=0.5)
        ax.legend()

        fig.tight_layout()
        return fig

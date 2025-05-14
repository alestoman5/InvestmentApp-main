"""Tkinter GUI for stock screening and backtesting."""

from __future__ import annotations
import tkinter as tk
from typing import Mapping, Type, Any

from utils.config import WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_COLOR, METRIC_CATEGORIES
from app.controller import Controller
from app.widgets import (
    DateSelector,
    MetricInput,
    RunButton,
    StrategySelector,
)


class InvestmentApp:
    """Main application for stock screening and backtesting."""

    def __init__(
        self,
        screener: Any,
        strategies: Mapping[str, Type[Any]],
    ) -> None:
        self.screener = screener
        self.strategies = strategies

        self.root = tk.Tk()
        self.root.title("Investment Backtest App")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)

        left_panel = tk.Frame(self.root, width=300, bg=BACKGROUND_COLOR)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(
            left_panel,
            text="Date Settings",
            bg=BACKGROUND_COLOR,
            font=("Arial", 10, "bold"),
        ).pack(anchor="w", padx=10, pady=2)

        self.date_selector = DateSelector(left_panel)
        self.date_selector.pack(anchor="w", padx=10, pady=2)

        self.metric_widgets: list[MetricInput] = []
        for header, metrics in METRIC_CATEGORIES.items():
            tk.Label(
                left_panel,
                text=header,
                bg=BACKGROUND_COLOR,
                font=("Arial", 10, "bold"),
            ).pack(anchor="w", padx=15, pady=2)

            for label, key in metrics:
                widget = MetricInput(left_panel, label, key)
                widget.pack(anchor="w", padx=15, pady=2)
                self.metric_widgets.append(widget)

        tk.Label(
            left_panel,
            text="Backtest Strategy",
            bg=BACKGROUND_COLOR,
            font=("Arial", 10, "bold"),
        ).pack(anchor="w", padx=10, pady=(5, 2))

        self.strategy_selector = StrategySelector(
            left_panel, list(self.strategies.keys())
        )
        self.strategy_selector.pack(anchor="w", padx=15, pady=2)

        self.controller = Controller(self, screener, strategies)
        self.run_button = RunButton(
            left_panel, command=self.controller.run_backtest
        )
        self.run_button.pack(padx=20, pady=5, fill=tk.X)

        bottom_panel = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        bottom_panel.pack(side=tk.BOTTOM, fill=tk.X)
        self.returns_label = self._create_section(
            bottom_panel, "Performance Statistics"
        )
        self.risk_label = self._create_section(
            bottom_panel, "Risk Statistics"
        )
        self.other_label = self._create_section(
            bottom_panel, "Other Statistics"
        )

        self.chart_frame = tk.Frame(self.root, bg="white")
        self.chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def _create_section(self, parent: tk.Frame, title: str) -> tk.Label:
        frame = tk.Frame(parent, bg=BACKGROUND_COLOR)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            frame,
            text=title,
            bg=BACKGROUND_COLOR,
            font=("Arial", 11, "bold"),
        ).pack(anchor="w", padx=10)

        label = tk.Label(
            frame,
            bg=BACKGROUND_COLOR,
            justify="left",
            font=("Arial", 12),
        )
        label.pack(anchor="w", padx=10)
        return label

    def run(self) -> None:
        """Start the Tkinter event loop."""
        self.root.mainloop()

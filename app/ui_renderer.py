"""UI renderer for updating the backtest GUI."""

from __future__ import annotations
from typing import Any, Tuple
import tkinter as tk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class UIRenderer:
    """Render and update GUI with backtest results."""

    def __init__(self, app: Any) -> None:
        self._app = app

    def prepare(self) -> None:
        """Disable run button and show busy cursor."""
        self._app.run_button.config(state=tk.DISABLED)
        self._app.root.config(cursor="watch")
        self._app.root.update()

    def render(self, result: Tuple[str, Any, str]) -> None:
        """Handle backtest outcome: error, warning, or display results."""
        status, strategy, message = result
        if status == "warn":
            messagebox.showwarning("No Stocks Found", message)
        elif status == "err":
            messagebox.showerror("Error", message)
        else:
            # Check for empty portfolio series
            series = getattr(strategy, "portfolio_series", None)
            if series is None or getattr(series, "empty", True):
                messagebox.showwarning(
                    "Empty Portfolio",
                    "Portfolio is empty, no data to display."
                )
            else:
                self._update(strategy)

        # Restore UI state
        self._app.root.config(cursor="")
        self._app.run_button.config(state=tk.NORMAL)

    def _update(self, strategy: Any) -> None:
        """Clear previous output and show new plot and stats."""
        # Clear old widgets
        for child in self._app.chart_frame.winfo_children():
            child.destroy()

        # Plot new figure
        fig: Figure = strategy.plot(self._app.chart_frame)
        canvas = FigureCanvasTkAgg(fig, master=self._app.chart_frame).get_tk_widget()
        canvas.pack(fill="both", expand=True)

        # Update stats labels
        stats = strategy.get_statistics()
        if stats:
            self._app.returns_label.config(
                text=(
                    f"Total Return: {stats.total_return:.2f}%\n"
                    f"Annual Return: {stats.annualized_return:.2f}%"
                )
            )
            self._app.risk_label.config(
                text=(
                    f"Volatility: {stats.volatility:.2f}%\n"
                    f"Max Drawdown: {stats.max_drawdown:.2f}%"
                )
            )
            self._app.other_label.config(
                text=(
                    f"Sharpe Ratio: {stats.sharpe_ratio:.2f}\n"
                    f"Win Rate: {stats.win_rate:.2f}%"
                )
            )
        self._app.root.update_idletasks()

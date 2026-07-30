"""Controller connecting GUI with backtesting logic."""

from __future__ import annotations
from typing import Mapping, Any, Tuple, Callable
from tkinter import messagebox

from app.inputs import InputCollector
from app.backtest_orchestrator import BacktestOrchestrator
from app.ui_renderer import UIRenderer


class Controller:
    """Orchestrate input validation, backtesting, and UI updates."""

    def __init__(
        self,
        app: Any,
        screener: Any,
        strategies: Mapping[str, type[Any]],
    ) -> None:
        self.validator = InputCollector(app)
        self.renderer = UIRenderer(app)
        # schedule backtest tasks on Tk event loop
        self.orchestrator = BacktestOrchestrator(
            screener, strategies, app.root
        )

    def run_backtest(self) -> None:
        """Trigger asynchronous backtest using validated inputs."""
        try:
            inputs = self.validator.collect()
        except ValueError as exc:
            messagebox.showwarning("Invalid Input", str(exc))
            return
        self.renderer.prepare()
        callback: Callable[[Tuple[str, Any, str]], None] = self.renderer.render
        self.orchestrator.run_backtest(inputs, callback)

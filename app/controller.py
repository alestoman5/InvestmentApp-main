"""Controller connecting GUI with backtesting logic."""

from __future__ import annotations
from typing import Mapping, Any, Tuple, Callable

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
        self._validator = InputCollector(app)
        self._renderer = UIRenderer(app)
        # schedule backtest tasks on Tk event loop
        self._orchestrator = BacktestOrchestrator(
            screener, strategies, app.root
        )

    def run_backtest(self) -> None:
        """Trigger asynchronous backtest using validated inputs."""
        try:
            inputs = self._validator.collect()
        except ValueError:
            return
        self._renderer.prepare()
        callback: Callable[[Tuple[str, Any, str]], None] = self._renderer.render
        self._orchestrator.run_backtest(inputs, callback)

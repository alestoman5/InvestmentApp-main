"""Asynchronous backtest orchestrator."""

from __future__ import annotations
import threading
import datetime as dt
from typing import Any, Mapping, Type, Callable, Tuple, Optional

import tkinter as tk

from app.inputs import UserInputDTO
from strategies.strategy_abstract import StrategyBase


class BacktestOrchestrator:
    """Run backtest in a background thread and schedule a callback."""

    def __init__(
        self,
        screener: Any,
        strategies: Mapping[str, Type[StrategyBase]],
        root: tk.Misc,
    ) -> None:
        self._screener = screener
        self._strategies = strategies
        self._root = root

    def run_backtest(
        self,
        input_data: UserInputDTO,
        callback: Callable[[Tuple[str, Optional[StrategyBase], Optional[str]]], None],
    ) -> None:
        """Start the backtest asynchronously."""
        thread = threading.Thread(
            target=self._worker,
            args=(input_data, callback),
            daemon=True,
        )
        thread.start()

    @staticmethod
    def dates_from_quarter(year: int, quarter: str) -> dt.date:
        """Return the last calendar day of the given year and quarter."""
        mapping = {"Q1": (3, 31), "Q2": (6, 30), "Q3": (9, 30), "Q4": (12, 31)}
        if quarter not in mapping:
            raise ValueError(f"Invalid quarter: {quarter}")
        month, day = mapping[quarter]
        start = dt.date(year, month, day)
        return start

    def _worker(
        self,
        input_data: UserInputDTO,
        callback: Callable[[Tuple[str, Optional[StrategyBase], Optional[str]]], None],
    ) -> None:
        """Background worker performing the backtest."""
        try:
            syear = input_data.syear
            squarter = input_data.squarter
            eyear = input_data.eyear
            equarter = input_data.equarter

            filters = input_data.filters
            name = input_data.strategy_name

            tickers = self._screener.filter_stocks(syear, squarter, filters)
            if not tickers:
                result = ("warn", None, "No stocks met criteria.")
            else:
                start = self.dates_from_quarter(syear, squarter)
                end = self.dates_from_quarter(eyear, equarter)
                strategy_cls = self._strategies.get(name)
                if not strategy_cls:
                    raise ValueError(f"Unknown strategy: {name}")
                strategy = strategy_cls(tickers, start, end)
                result = ("ok", strategy, None)
        except Exception as e:
            result = ("err", None, str(e))

        self._root.after(0, callback, result)

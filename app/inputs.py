"""Data transfer object and validator for user inputs."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class UserInputDTO:
    """User inputs: year, quarter, filters, and strategy name."""
    year: int
    quarter: str
    filters: Dict[str, Tuple[str, float]]
    strategy_name: str


class InputCollector:
    """Collect and validate user input from the GUI."""

    def __init__(self, app: Any) -> None:
        self._app = app

    def collect(self) -> UserInputDTO:
        """Return DTO with current selections from the UI."""
        year, quarter = self._app.date_selector.get_date()
        filters: Dict[str, Tuple[str, float]] = {}

        for widget in self._app.metric_widgets:
            cond = widget.condition_var.get()
            val = widget.get_value()
            # user chose Over/Under but get_value() returned None → invalid
            if cond != "Any" and val is None:
                raise ValueError(f"Invalid input for {widget.key}")
            if val is not None:
                filters[widget.key] = val

        strategy = self._app.strategy_selector.get_selected()
        return UserInputDTO(year, quarter, filters, strategy)

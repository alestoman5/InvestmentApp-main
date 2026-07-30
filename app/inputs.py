"""Data transfer object and validator for user inputs."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class UserInputDTO:
    """User inputs: year, quarter, filters, and strategy name."""
    syear: int
    squarter: str
    eyear: int
    equarter: str
    filters: Dict[str, Tuple[str, float]]
    strategy_name: str


class InputCollector:
    """Collect and validate user input from the GUI."""

    def __init__(self, app: Any) -> None:
        self._app = app

    def collect(self) -> UserInputDTO:
        """Return DTO with current selections from the UI."""
        syear, squarter = self._app.date_selector.get_date()
        eyear, equarter = self._app.end_selector.get_date()

        # Quarter labels sort lexicographically, so tuple comparison works.
        if (syear, squarter) >= (eyear, equarter):
            raise ValueError(
                f"End date ({eyear} {equarter}) must be after "
                f"start date ({syear} {squarter})."
            )

        filters: Dict[str, Tuple[str, float]] = {}
        for widget in self._app.metric_widgets:
            val = widget.get_value()
            if val is not None:
                filters[widget.key] = val

        strategy = self._app.strategy_selector.get_selected()
        return UserInputDTO(syear, squarter, eyear, equarter, filters, strategy)

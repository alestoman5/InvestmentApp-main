"""Reusable Tkinter widgets for the investment GUI."""

from __future__ import annotations
from typing import Sequence, Optional, Callable, Tuple
import tkinter as tk
from tkinter import Frame, StringVar, Label, OptionMenu, Radiobutton, Spinbox, Button
import datetime as dt

from utils.config import BACKGROUND_COLOR


class DateSelector(Frame):
    """Select year and quarter."""

    def __init__(
        self,
        master: tk.Misc,
        years: Optional[Sequence[int]] = None,
        default_year: Optional[int] = None,
        default_quarter: str = "Q1",
    ) -> None:
        super().__init__(master, bg=BACKGROUND_COLOR)

        # Fall back to a generic range only if the data source offers nothing.
        year_values = list(years) if years else list(
            range(2010, dt.datetime.now().year + 1)
        )
        self._year = StringVar(
            value=str(default_year if default_year is not None else year_values[0])
        )
        self._quarter = StringVar(value=default_quarter)

        years_str = [str(y) for y in year_values]
        quarters = ["Q1", "Q2", "Q3", "Q4"]

        Label(self, text="Year:", bg=BACKGROUND_COLOR).grid(row=0, column=0, sticky="e", padx=5, pady=2)
        year_menu = OptionMenu(self, self._year, *years_str)
        year_menu.config(width=6)
        year_menu.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        Label(self, text="Quarter:", bg=BACKGROUND_COLOR).grid(row=0, column=2, sticky="e", padx=5, pady=2)
        quarter_menu = OptionMenu(self, self._quarter, *quarters)
        quarter_menu.config(width=3)
        quarter_menu.grid(row=0, column=3, sticky="w", padx=5, pady=2)

    def get_date(self) -> Tuple[int, str]:
        return int(self._year.get()), self._quarter.get()


class MetricInput(Frame):
    """Input for a single metric filter."""

    def __init__(
        self,
        master: tk.Misc,
        label: str,
        key: str,
    ) -> None:
        super().__init__(master, bg=BACKGROUND_COLOR)
        self.key: str = key
        self.label: str = label
        self.condition_var = StringVar(value="Any")

        Label(self, text=label, width=20, anchor="w", bg=BACKGROUND_COLOR).pack(side=tk.LEFT, padx=5)
        cond_menu = OptionMenu(self, self.condition_var, "Any", "Over", "Under")
        cond_menu.config(width=5)
        cond_menu.pack(side=tk.LEFT, padx=5)

        self._spin_val = Spinbox(self, from_=0, to=500, width=6, justify="center")
        self._spin_val.pack(side=tk.LEFT, padx=5)

    def get_value(self) -> Optional[Tuple[str, float]]:
        """Return (condition, threshold), or None when set to 'Any'.

        Raises ValueError if the threshold is not a number.
        """
        cond = self.condition_var.get()
        if cond == "Any":
            return None
        try:
            val = float(self._spin_val.get())
        except ValueError:
            raise ValueError(f"{self.label}: '{self._spin_val.get()}' is not a number.")
        return cond, val


class StrategySelector(Frame):
    """Select backtest strategy."""

    def __init__(
        self,
        master: tk.Misc,
        options: Sequence[str],
    ) -> None:
        super().__init__(master, bg=BACKGROUND_COLOR)
        default = options[0] if options else ""
        self._strategy = StringVar(value=default)

        for opt in options:
            Radiobutton(
                self,
                text=opt,
                variable=self._strategy,
                value=opt,
                bg=BACKGROUND_COLOR,
            ).pack(anchor="w", padx=10)

    def get_selected(self) -> str:
        return self._strategy.get()


class RunButton(Button):
    """Button to start backtest."""

    def __init__(
        self,
        master: tk.Misc,
        command: Callable[[], None],
    ) -> None:
        super().__init__(
            master,
            text="Run Backtest",
            bg="red",
            fg="white",
            font=("Arial", 12, "bold"),
            command=command,
        )

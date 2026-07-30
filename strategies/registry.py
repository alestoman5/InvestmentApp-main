"""Registry mapping display names to strategy classes."""

from __future__ import annotations
from typing import Callable, Type

from strategies.strategy_abstract import StrategyBase

REG: dict[str, Type[StrategyBase]] = {}


def register_strategy(
    name: str,
) -> Callable[[Type[StrategyBase]], Type[StrategyBase]]:
    """Register a strategy class under a display name."""
    def deco(cls: Type[StrategyBase]) -> Type[StrategyBase]:
        REG[name] = cls
        return cls
    return deco

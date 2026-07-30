"""Strategy package: importing it registers every built-in strategy."""

from .registry import REG, register_strategy
from .buy_and_hold import BuyAndHoldStrategy
from .periodic_rebalance import PeriodicRebalanceStrategy

__all__ = [
    "REG",
    "register_strategy",
    "BuyAndHoldStrategy",
    "PeriodicRebalanceStrategy",
]

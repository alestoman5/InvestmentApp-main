from typing import Type
from strategies.strategy_abstract import StrategyBase


_REG: dict[str,Type[StrategyBase]] = {}

def register_strategy(name:str):
    def deco(cls):
        _REG[name] = cls
        return cls
    return deco
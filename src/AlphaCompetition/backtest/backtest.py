from pydantic import BaseModel
from utils.utils import EnhancedStrEnum
from numpy.typing import NDArray

import pandas as pd
import numpy as np


class BacktestResult(EnhancedStrEnum):
    PROFIT: str = 'PROFIT'
    LOSS: str = 'LOSS'
    UNAVAILABLE: str = 'UNAVAILABLE'


class BacktestSummary:
    dataset_reference_name: str
    start_index: int
    end_index: int
    entry_point: float
    take_profit: float
    stop_loss: float
    result: BacktestResult
    numerical_result: float

class BacktestSingleton(type):
    _instance = None

    def __call__(self, *args, **kwds):
        if not self._instance:
            super().__call__(*args, **kwds)
        
        return self._instance


class Backtest(
    metaclass=BacktestSingleton
):
    def __init__(self,
                 df: pd.DataFrame) -> None:
        self._dataset_reference: pd.DataFrame = df
        self._summary: list[BacktestSummary] = []

    def backtest(
            self,
            side: bool,
            start_index: int,
            take_profit: np.float64 | float,
            stop_loss: np.float64 | float,
        ) -> BacktestSummary:
        vector: NDArray = self._dataset_reference.loc[start_index:, :]
        entry_point: np.float64 = vector[0]
        
        if side:
            tp_value: np.float64 = entry_point + take_profit
            sl_value: np.float64 = entry_point - stop_loss

            tp_point: int = np.argmax(entry_point >= tp_value)
            sl_point: int = np.argmax(entry_point <= sl_value)
        else:
            tp_value: np.float64 = entry_point - take_profit
            sl_value: np.float64 = entry_point + stop_loss

            tp_point: int = np.argmax(entry_point <= tp_value)
            sl_point: int = np.argmax(entry_point >= sl_value)

            result = BacktestResult.PROFIT

        summary = BacktestSummary(
            dataset_reference_name='',
            start_index=start_index,
            end_index=...,
            entry_point=entry_point,
            take_profit=tp_value,
            stop_loss=sl_value,
            result=BacktestResult.PROFIT,
            numerical_value=0,
        )
        self._summary.append(summary)

    def summary(
            self,
        ) -> list[BacktestSummary]:
        return self._summary
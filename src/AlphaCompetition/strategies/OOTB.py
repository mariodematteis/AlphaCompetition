from data.data import Symbol
from log.log import Logger
from numpy.typing import NDArray
from backtest.backtest import Backtest, BacktestSummary

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

class OutOfTheBox:
    def __init__(self):
        self.logger = Logger('OutOfTheBox')
        self.symbol = Symbol()
        self.sp500_tickers: list[str] = self.symbol.get_standard_and_poors()
        self._tmp_distributions: dict[str, pd.DataFrame] = {}
        self.pos_neg_distribution: dict[str, list[NDArray]] = {}
        self._distance_distribution: pd.Series = pd.Series()

    def tickers(self) -> list[str]:
        return self.sp500_tickers
    
    def _distributions(self,
                      time_frame: str = '1m',
                      start_date: str = '2023-01-01',
                      end_date: str = '2023-12-31') -> None:
        for ticker in self.sp500_tickers:
            self.logger.info(f'Fetching Prices from {ticker}')
            df_ticker = yf.download(tickers=ticker, 
                                    start=start_date,
                                    end=end_date,
                                    interval=time_frame)
            self._tmp_distributions[ticker] = df_ticker['Adj Close'].pct_change().dropna().to_numpy()

    def _process_distributions(self) -> None:
        for ticker, distribution in self._tmp_distributions.items():
            self.pos_neg_distribution[ticker] = [
                distribution[distribution > 0],
                distribution[distribution < 0]
            ]
        
    def _kullback_leibler_divergence(self, 
                                     p: NDArray,
                                     q: NDArray) -> np.float64:
        return np.sum(np.where(((p != 0) | (p != np.inf)), p * np.log(p / q), 0))
    
    def pad_to_same_length(self, a, b) -> tuple[NDArray]:
        min_length = min(len(a), len(b))
        a_padded = np.random.choice(a, 
                                    size=min_length, 
                                    replace=False)
        b_padded = np.random.choice(b, 
                                    size=min_length, 
                                    replace=False)
        return a_padded, b_padded


    def _process_distance(self) -> None:
        for ticker, distribution in self.pos_neg_distribution.items():
            t_p_dist, t_n_dist = self.pad_to_same_length(
                np.abs(distribution[0]), 
                np.abs(distribution[1])
            )
            positive_distribution: NDArray = np.abs(t_p_dist)
            negative_distribution: NDArray = np.abs(t_n_dist)

            norm_pos_dist: NDArray = positive_distribution / np.sum(positive_distribution)
            norm_neg_dist: NDArray = negative_distribution / np.sum(negative_distribution)

            self._distance_distribution[ticker] = self._kullback_leibler_divergence(norm_pos_dist, norm_neg_dist)

    def _select_tickers(self,
                        percentile: float = 0.2) -> int:
        self._distance_distribution.sort_values(ascending=False)
        return int(self._distance_distribution.quantile(
                q=percentile
            ))
    
    def _plot_distance_distributions(self, 
                                     bins: int = 50) -> None:
        _, ax = plt.subplots(figsize=(20, 8))
        ax.hist(self._distance_distribution.values, 
                bins=bins)
        plt.show()

    def analyze(self,
                time_frame: str = '1m',
                start_date: str = '2023-01-01',
                end_date: str = '2023-12-31') -> None:
        self._distributions(time_frame=time_frame,
                            start_date=start_date,
                            end_date=end_date)
        self._process_distributions()
        self._process_distance()
        index = self._select_tickers()
        self._plot_distance_distributions()
        selected_ticker = self._distance_distribution[:index + 1]

    def backtest(self) -> list[BacktestSummary]:
        backtest = Backtest()
        backtest.backtest()

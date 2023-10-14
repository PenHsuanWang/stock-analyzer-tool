"""
This module define the single responsibility to do numeric calculating related with time based computing.
"""

import pandas as pd

def calculate_moving_average(data_series: pd.Series, window_size: int) -> pd.Series:
    """
    Calculate the moving average of a given pandas Series.

    :param data_series: pandas Series of data points
    :param window_size: integer, size of the rolling window
    :return: pandas Series of moving averages
    """
    return data_series.rolling(window=window_size).mean()


def calculate_daily_return(data_series: pd.Series) -> pd.Series:
    """
    Calculate the daily return rate of a given pandas Series.

    :param data_series: pandas Series of data points (e.g., closing prices)
    :return: pandas Series of daily return rates
    """
    return data_series.pct_change().fillna(0)


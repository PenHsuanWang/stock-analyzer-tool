import pandas as pd
from src.stockana import calc_time_based


def test_calculate_moving_average():
    data = pd.Series([1, 2, 3, 4, 5])
    result = calc_time_based.calculate_moving_average(data, 2)
    expected = pd.Series([None, 1.5, 2.5, 3.5, 4.5])
    pd.testing.assert_series_equal(result, expected, check_dtype=False)


def test_calculate_daily_return():
    data = pd.Series([100, 101, 102, 101, 100])
    result = calc_time_based.calculate_daily_return(data)
    expected = pd.Series([0, 0.01, 0.00990099, -0.00980392, -0.00990099])
    assert all((result - expected).abs() < 1e-7)  # Compare with a small tolerance due to floating point arithmetic


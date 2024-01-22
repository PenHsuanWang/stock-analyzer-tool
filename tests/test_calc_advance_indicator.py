import pytest
import pandas as pd
from src.stockana.calc_advance_indicator import AdvancedFinancialIndicator


# Sample data for testing
data = {
    'Date': ['2021-01-01', '2021-01-02', '2021-01-03', '2021-01-04', '2021-01-05'],
    'Close': [100, 102, 101, 105, 107],
    'Volume': [200, 220, 210, 240, 230],
    'High': [102, 103, 102, 106, 108],
    'Low': [98, 101, 100, 104, 106]
}
sample_df = pd.DataFrame(data)
sample_df['Date'] = pd.to_datetime(sample_df['Date'])
sample_df.set_index('Date', inplace=True)


@pytest.fixture
def stock_data():
    return sample_df.copy()


@pytest.fixture
def empty_data():
    return pd.DataFrame()


# Testing EMA Calculation
def test_compute_ema(stock_data):
    result = AdvancedFinancialIndicator.compute_ema(stock_data, window=2, column='Close')
    assert not result.empty
    assert result.iloc[-1] == pytest.approx(106.75, 0.01)  # Check last EMA value


# Testing EMA Calculation with empty data
def test_compute_ema_empty(empty_data):
    with pytest.raises(KeyError):
        AdvancedFinancialIndicator.compute_ema(empty_data, window=2, column='Close')


# Test EMA with invalid window size
def test_compute_ema_invalid_window(stock_data):
    with pytest.raises(ValueError):
        AdvancedFinancialIndicator.compute_ema(stock_data, window=-1, column='Close')


# Testing MACD Calculation
def test_compute_macd(stock_data):
    macd_series, signal_line_series, macd_histogram_series = AdvancedFinancialIndicator.compute_macd(stock_data)

    # Check if MACD, Signal Line, and Histogram are all pd.Series
    assert isinstance(macd_series, pd.Series), "MACD should be a pandas Series."
    assert isinstance(signal_line_series, pd.Series), "Signal Line should be a pandas Series."
    assert isinstance(macd_histogram_series, pd.Series), "MACD Histogram should be a pandas Series."

    # Check if the lengths of the returned series match the length of the input DataFrame
    assert len(macd_series) == len(stock_data), "Length of MACD series should match input DataFrame."
    assert len(signal_line_series) == len(stock_data), "Length of Signal Line series should match input DataFrame."
    assert len(macd_histogram_series) == len(stock_data), "Length of MACD Histogram series should match input DataFrame."

    # Check if MACD Histogram is indeed the difference between MACD and Signal Line
    assert all(macd_histogram_series == (macd_series - signal_line_series)), "MACD Histogram should be the difference between MACD and Signal Line."


# Testing Bollinger Bands Calculation
def test_compute_bollinger_bands(stock_data):
    bollinger_upper, bollinger_mid, bollinger_lower = AdvancedFinancialIndicator.compute_bollinger_bands(stock_data)

    # Check if all three Bollinger bands are pd.Series
    assert isinstance(bollinger_upper, pd.Series), "Bollinger Upper should be a pandas Series."
    assert isinstance(bollinger_mid, pd.Series), "Bollinger Middle should be a pandas Series."
    assert isinstance(bollinger_lower, pd.Series), "Bollinger Lower should be a pandas Series."

    assert len(bollinger_upper) == len(stock_data), "Length of Bollinger Upper series should match input DataFrame."
    assert len(bollinger_mid) == len(stock_data), "Length of Bollinger Middle series should match input DataFrame."
    assert len(bollinger_lower) == len(stock_data), "Length of Bollinger Lower series should match input DataFrame."


# Testing RSI Calculation
def test_compute_rsi(stock_data):
    rsi_series = AdvancedFinancialIndicator.compute_rsi(stock_data)

    # Check if the RSI is a pd.Series
    assert isinstance(rsi_series, pd.Series), "RSI should be a pandas Series."

    assert len(rsi_series) == len(stock_data), "Length of RSI series should match input DataFrame."


# Testing Fibonacci Retracement Calculation
def test_compute_fibonacci_retracement(stock_data):
    stock_data_reset = stock_data.reset_index()  # Reset index to make 'Date' a column
    levels = AdvancedFinancialIndicator.compute_fibonacci_retracement(stock_data_reset, '2021-01-01', '2021-01-05')
    assert isinstance(levels, dict)
    assert 'Level_0' in levels and 'Level_100' in levels


# Test Fibonacci Retracement with invalid date range
def test_compute_fibonacci_retracement_invalid_date(stock_data):
    with pytest.raises(ValueError):
        _ = AdvancedFinancialIndicator.compute_fibonacci_retracement(stock_data, '2021-01-10', '2021-01-15')


# Testing Combined Strategy Application
def test_apply_strategy(stock_data):
    result = AdvancedFinancialIndicator.apply_strategy(stock_data, short_window=2, long_window=5, signal_window=3, volume_window=20)
    assert all(key in result for key in ['Buy_Signal', 'Sell_Signal'])


# Test MACD with valid data
def test_compute_macd_valid(stock_data):
    macd_series, signal_line_series, macd_histogram_series = AdvancedFinancialIndicator.compute_macd(stock_data)

    # Check if MACD, Signal Line, and Histogram are pd.Series
    assert isinstance(macd_series, pd.Series), "MACD should be a pandas Series."
    assert isinstance(signal_line_series, pd.Series), "Signal Line should be a pandas Series."
    assert isinstance(macd_histogram_series, pd.Series), "MACD Histogram should be a pandas Series."

    # Optionally, check if they have the same length as the input DataFrame
    assert len(macd_series) == len(stock_data), "Length of MACD series should match input DataFrame."
    assert len(signal_line_series) == len(stock_data), "Length of Signal Line series should match input DataFrame."


# Test MACD with empty data
def test_compute_macd_empty(empty_data):
    macd_series, signal_line_series, macd_histogram_series = AdvancedFinancialIndicator.compute_macd(empty_data)

    # Check if MACD, Signal Line, and Histogram are None for empty input
    assert macd_series is None, "For empty data, MACD should be None."
    assert signal_line_series is None, "For empty data, Signal Line should be None."
    assert macd_histogram_series is None, "For empty data, MACD Histogram should be None."



# Test Bollinger Bands with valid data
def test_compute_bollinger_bands_valid(stock_data):
    bollinger_upper, bollinger_mid, bollinger_lower = AdvancedFinancialIndicator.compute_bollinger_bands(stock_data)

    # Check if all three Bollinger bands are pd.Series
    assert isinstance(bollinger_upper, pd.Series), "Bollinger Upper should be a pandas Series."
    assert isinstance(bollinger_mid, pd.Series), "Bollinger Middle should be a pandas Series."
    assert isinstance(bollinger_lower, pd.Series), "Bollinger Lower should be a pandas Series."

    # Optionally, check if they have the same length as the input DataFrame
    assert len(bollinger_upper) == len(stock_data), "Length of Bollinger Upper series should match input DataFrame."
    assert len(bollinger_mid) == len(stock_data), "Length of Bollinger Middle series should match input DataFrame."
    assert len(bollinger_lower) == len(stock_data), "Length of Bollinger Lower series should match input DataFrame."


# Test Bollinger Bands with empty data
def test_compute_bollinger_bands_empty(empty_data):
    bollinger_upper, bollinger_mid, bollinger_lower = AdvancedFinancialIndicator.compute_bollinger_bands(empty_data)

    # Check if all three Bollinger bands are None for empty input
    assert bollinger_upper is None, "Bollinger Upper should be None for empty input."
    assert bollinger_mid is None, "Bollinger Middle should be None for empty input."
    assert bollinger_lower is None, "Bollinger Lower should be None for empty input."


# Test RSI with valid data
def test_compute_rsi_valid(stock_data):
    rsi_series = AdvancedFinancialIndicator.compute_rsi(stock_data)

    # Check if the RSI is a pd.Series
    assert isinstance(rsi_series, pd.Series), "RSI should be a pandas Series."

    # Optionally, check if it has the same length as the input DataFrame
    assert len(rsi_series) == len(stock_data), "Length of RSI series should match input DataFrame."


# Test RSI with empty data
def test_compute_rsi_empty(empty_data):
    rsi_series = AdvancedFinancialIndicator.compute_rsi(empty_data)

    # Check if None is returned for empty input
    assert rsi_series is None, "For empty data, RSI should be None."


# Test Combined Strategy with valid data
def test_apply_strategy_valid(stock_data):
    result = AdvancedFinancialIndicator.apply_strategy(stock_data, short_window=12, long_window=26, signal_window=9, volume_window=20)

    # Check if new columns have been added to the DataFrame
    for column in ['MACD', 'Signal_Line', 'MACD_Histogram', 'Bollinger_Upper', 'Bollinger_Mid', 'Bollinger_Lower', 'RSI', 'Buy_Signal', 'Sell_Signal']:
        assert column in result.columns, f"{column} column should be in the result DataFrame."

    # Optionally, check the logic of signals according to the defined strategy
    # This could involve checking that 'Buy_Signal' is True where expected and False otherwise
    # Similar logic would apply for 'Sell_Signal'

    # Check that signals are not generated for all rows (depends on strategy logic)
    assert result['Buy_Signal'].sum() < len(result), "Not all rows should have a buy signal."
    assert result['Sell_Signal'].sum() < len(result), "Not all rows should have a sell signal."


# Test Combined Strategy with empty data
def test_apply_strategy_empty(empty_data):
    result = AdvancedFinancialIndicator.apply_strategy(empty_data, short_window=12, long_window=26, signal_window=9, volume_window=20)

    # Check if the result DataFrame is unchanged for empty input (if that's the expected behavior)
    assert result.empty or result.equals(empty_data), "Result should be an empty DataFrame or equal to the input empty DataFrame for empty input data."

    # Alternatively, if the method is expected to return a DataFrame with the new columns but no data, check for that
    expected_columns = ['MACD', 'Signal_Line', 'MACD_Histogram', 'Bollinger_Upper', 'Bollinger_Mid', 'Bollinger_Lower', 'RSI', 'Buy_Signal', 'Sell_Signal']
    if not result.empty:
        for column in expected_columns:
            assert column in result.columns, f"{column} column should be present even if the input data is empty."
            assert result[column].empty, f"{column} column should be empty for empty input data."


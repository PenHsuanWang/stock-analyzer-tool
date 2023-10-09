import pandas as pd
import pytest
from src.analyzer.stock_analyzer import StockPriceAnalyzer
import math

# Create a sample DataFrame for testing
def create_test_data():
    data = {
        "Date": pd.date_range(start="2022-01-01", periods=10, freq='D'),
        "Adj Close": [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
    }
    df = pd.DataFrame(data)
    return df

# Fixture to create an instance of StockPriceAnalyzer with test data
@pytest.fixture
def stock_analyzer():
    return StockPriceAnalyzer(create_test_data())


# Test calculating_moving_average
def test_calculating_moving_average(stock_analyzer):
    stock_analyzer.calculating_moving_average(window_size=3)
    analysis_data = stock_analyzer.get_analysis_data()
    assert "MA_3_days" in analysis_data.columns
    expected_values = [math.nan, math.nan, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0]
    for i, value in enumerate(analysis_data["MA_3_days"]):
        if i == 0:
            assert math.isnan(value)
        else:
            assert math.isnan(value) or math.isclose(value, expected_values[i])


# Test get_analysis_data
def test_get_analysis_data(stock_analyzer):
    analysis_data = stock_analyzer.get_analysis_data()
    assert isinstance(analysis_data, pd.DataFrame)
    assert len(analysis_data) == 10
    assert "Adj Close" in analysis_data.columns

# test_data_fetcher.py

import pandas as pd
from unittest.mock import patch, Mock
import pytest
from requests.exceptions import HTTPError
from src.data_io.data_fetcher import YFinanceFetcher


# Mock the yf.Ticker() call to avoid actual network requests
def mock_yf_ticker(info=None):
    mock_ticker = Mock()
    mock_ticker.info = info
    return mock_ticker


@pytest.fixture
def yfinance_fetcher():
    return YFinanceFetcher()


# === test cases for `_extract_fetch_stock_and_time_range_params`

def test_valid_params(yfinance_fetcher):
    with patch('src.data_io.data_fetcher.yf.Ticker', side_effect=mock_yf_ticker):
        result = yfinance_fetcher._extract_fetch_stock_and_time_range_params(
            stock_id="AAPL",
            start_date="2022-01-01",
            end_date="2022-12-31"
        )
        assert result == ("AAPL", "2022-01-01", "2022-12-31")


def test_missing_parameters(yfinance_fetcher):
    with pytest.raises(ValueError, match="Missing input parameters"):
        yfinance_fetcher._extract_fetch_stock_and_time_range_params()


def test_invalid_stock_id(yfinance_fetcher):
    with patch('src.data_io.data_fetcher.yf.Ticker', side_effect=HTTPError()):
        with pytest.raises(ValueError, match="Invalid stock id: ABC"):
            yfinance_fetcher._extract_fetch_stock_and_time_range_params(
                stock_id="ABC",
                start_date="2022-01-01",
                end_date="2022-12-31"
            )


def test_invalid_date_format(yfinance_fetcher):
    with pytest.raises(ValueError, match="Invalid date format"):
        yfinance_fetcher._extract_fetch_stock_and_time_range_params(
            stock_id="AAPL",
            start_date="2022-01-01",
            end_date=20221231  # Invalid date format
        )


def test_invalid_date_range(yfinance_fetcher):
    with pytest.raises(ValueError, match="Invalid date range"):
        yfinance_fetcher._extract_fetch_stock_and_time_range_params(
            stock_id="AAPL",
            start_date="2022-12-31",  # End date before start date
            end_date="2022-01-01"
        )


# ===== test cases for `fetch_from_source`

def test_fetch_from_source_empty_data(yfinance_fetcher):
    yfinance_fetcher._fetched_data = pd.DataFrame()  # Set _fetched_data to an empty DataFrame
    yfinance_fetcher.fetch_from_source(stock_id="AAPL", start_date="2022-01-01", end_date="2022-12-31")
    assert yfinance_fetcher._fetched_data.shape != (0, 0)


# ===== test cases for `get_as_dataframe`

def test_get_as_dataframe_valid_data(yfinance_fetcher):
    data = pd.DataFrame({"Date": ["2022-01-01", "2022-01-02"], "Close": [100, 101]})
    yfinance_fetcher._fetched_data = data
    result = yfinance_fetcher.get_as_dataframe()
    assert result.shape == (2, 2)


def test_get_as_dataframe_invalid_data(yfinance_fetcher):
    yfinance_fetcher._fetched_data = None  # Set _fetched_data to None
    with pytest.raises(ValueError, match="Invalid fetched data format"):
        yfinance_fetcher.get_as_dataframe()

import pytest
import pandas as pd
from src.stockana.calc_market_condition import MarketConditionLabeler


@pytest.fixture
def sample_data():
    data = {
        'Date': pd.date_range(start='2020-01-01', periods=100, freq='D'),
        'Close': [100 + i * (0.01 * i) for i in range(100)]  # Sample close prices
    }
    df = pd.DataFrame(data)
    df.set_index('Date', inplace=True)
    return df


def test_market_condition_labels(sample_data):
    market_condition = MarketConditionLabeler(sample_data)
    labeled_series = market_condition.label_market()

    assert labeled_series.iloc[19] == 'Neutral'
    assert labeled_series.iloc[20] == 'Mild Bull Market'
    assert labeled_series.iloc[99] == 'Moderate Bull Market'


def test_rolling_return_calculation(sample_data):
    market_condition = MarketConditionLabeler(sample_data)
    labeled_df = sample_data
    labeled_df["Market Condition"] = market_condition.label_market()

    # check the 21st day's rolling calculation is correct
    expected_return_day_21 = sample_data['Close'].pct_change().iloc[1:21].sum()
    assert labeled_df['Rolling Return'].iloc[20] == pytest.approx(expected_return_day_21, 0.01)

    # check the 50th day's rolling calculation is correct
    expected_return_day_50 = sample_data['Close'].pct_change().iloc[30:50].sum()
    assert labeled_df['Rolling Return'].iloc[49] == pytest.approx(expected_return_day_50, 0.01)


def test_empty_data():
    empty_df = pd.DataFrame(columns=['Date', 'Close'])
    empty_df.set_index('Date', inplace=True)
    market_condition = MarketConditionLabeler(empty_df)
    labeled_df = market_condition.label_market()
    assert labeled_df.empty


def test_constant_price():
    constant_price_df = pd.DataFrame({
        'Date': pd.date_range(start='2020-01-01', periods=50, freq='D'),
        'Close': [100 for _ in range(50)]
    })
    constant_price_df.set_index('Date', inplace=True)
    market_condition = MarketConditionLabeler(constant_price_df)
    labeled_df = market_condition.label_market()

    assert all(labeled_df == 'Neutral')

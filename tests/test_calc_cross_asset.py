import pytest
import pandas as pd
from src.stockana.calc_cross_asset import calculate_correlation  # Replace 'your_module_name' with the actual name of your module


def test_calculate_correlation():
    # Create sample Series
    s1 = pd.Series([1, 2, 3, 4, 5])
    s2 = pd.Series([5, 4, 3, 2, 1])
    s3 = pd.Series([1, 3, 5, 7, 9])

    # Call the function
    result = calculate_correlation([s1, s2, s3])

    # Check the shape of the result
    assert result.shape == (3, 3), "The result should be a 3x3 DataFrame"

    # Check the correlation values
    assert result.iloc[0, 1] == -1, "s1 and s2 should be perfectly inversely correlated"
    assert result.iloc[0, 2] > 0, "s1 and s3 should be positively correlated"
    assert result.iloc[1, 2] < 0, "s2 and s3 should be inversely correlated"

# Optional: Add more tests for edge cases, such as empty input, non-numeric data, etc.

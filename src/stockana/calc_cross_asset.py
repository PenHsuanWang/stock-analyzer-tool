import pandas as pd


def calculate_correlation(series_list: list[pd.Series]) -> pd.DataFrame:
    """
    Calculate the correlation between all pairs of pandas Series in the given list.

    :param series_list: list of pandas Series.
    :return: DataFrame, containing correlation coefficients between all pairs of Series.
    """
    # Construct a DataFrame with the given series
    df = pd.concat(series_list, axis=1)

    # Use the built-in .corr() method to calculate pairwise correlations
    correlation_df = df.corr()

    return correlation_df

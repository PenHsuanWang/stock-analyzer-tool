import pandas as pd

class CorrelationAnalyzer:
    """Class for analyzing correlations between multiple companies' stock daily returns."""

    def __init__(self, companies_data: dict[str, pd.DataFrame]):
        """
        Initialize with a dictionary of multiple companies' data.
        :param companies_data: A dictionary with company tickers as keys and their dataframes as values.
        """
        self._companies_data = companies_data

    def compute_daily_returns(self):
        """
        Compute daily returns for all companies in the dataset.
        :return: A dictionary with company tickers as keys and their daily returns dataframes as values.
        """
        daily_returns = {}
        for ticker, data in self._companies_data.items():
            data['Daily Return'] = data['Adj Close'].pct_change()
            daily_returns[ticker] = data['Daily Return']
        return daily_returns

    def compute_correlations(self):
        """
        Compute pairwise correlations between stock daily returns.
        :return: A dataframe containing pairwise correlations.
        """
        # Concatenate daily returns dataframes
        combined_data = pd.concat(self.compute_daily_returns(), axis=1)
        return combined_data.corr()

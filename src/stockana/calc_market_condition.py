import pandas as pd


class MarketConditionLabeler:
    """
    This class labels market condition based on rolling returns.
    """

    def __init__(self, data: pd.DataFrame, window_size: int = 20):
        """
        :param data: DataFrame containing stock data with 'Close' prices.
        :param window_size: Integer, the rolling window size to calculate rolling return.
        """
        self.data = data
        self.window_size = window_size
        self._calculate_rolling_return()

    def _calculate_rolling_return(self):
        """
        Calculate rolling return over a specified window size.
        """
        if not self.data.empty:
            self.data['Rolling Return'] = self.data['Close'].pct_change().rolling(window=self.window_size).sum()
        else:
            self.data['Rolling Return'] = pd.Series()

    def label_market(self):
        """
        Label the market condition based on rolling return.
        """
        def label(rolling_return):
            if rolling_return <= -0.20:
                return "Severe Bear Market"
            elif -0.20 < rolling_return <= -0.10:
                return "Moderate Bear Market"
            elif -0.10 < rolling_return < 0:
                return "Mild Bear Market"
            elif rolling_return == 0:
                return "Neutral"
            elif 0 < rolling_return < 0.10:
                return "Mild Bull Market"
            elif 0.10 <= rolling_return < 0.20:
                return "Moderate Bull Market"
            elif rolling_return >= 0.20:
                return "Strong Bull Market"
            return "Neutral"

        self.data['Market Condition'] = self.data['Rolling Return'].apply(label)

        return self.data['Market Condition']

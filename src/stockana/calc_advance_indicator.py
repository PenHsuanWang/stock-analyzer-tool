import logging
import pandas as pd
from typing import List, Dict, Tuple, Optional

# Initialize logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AdvancedFinancialIndicator:
    """
    Class to combine multiple financial analysis strategies: Moving Average,
    Volume Analysis, Bollinger Bands, MACD, and RSI and Fibonacci Retracement.
    """

    @staticmethod
    def validate_data(stock_data: pd.DataFrame, required_columns: List[str]) -> bool:
        """
        Validate if the required columns are present in the DataFrame.

        :param stock_data: DataFrame to be validated.
        :param required_columns: List of column names that are required.
        :return: True if all required columns are present, False otherwise.
        """
        missing_columns = [col for col in required_columns if col not in stock_data.columns]
        if missing_columns:
            logger.error(f"Missing required columns: {missing_columns}")
            return False
        return True

    @staticmethod
    def compute_ema(stock_data: pd.DataFrame, window: int, column: str = 'Close') -> pd.Series:
        """
        Compute Exponential Moving Average (EMA) for a given column.

        EMA is a type of moving average that places a greater weight and significance
        on the most recent data points. It's commonly used to identify the direction
        of a trend or to determine its strength.

        :param stock_data: DataFrame containing stock data.
        :param window: Integer representing the period of the EMA.
        :param column: The column on which EMA is to be computed.
        :return: Series containing the computed EMA values.
        """
        return stock_data[column].ewm(span=window, adjust=False).mean()

    @staticmethod
    def compute_macd(stock_data: pd.DataFrame, short_window: int = 12, long_window: int = 26,
                     signal_window: int = 9) -> Tuple[Optional[pd.Series], Optional[pd.Series]]:
        """
        Compute Moving Average Convergence Divergence (MACD) and Signal Line.

        MACD is a trend-following momentum indicator that shows the relationship between
        two moving averages of a security's price. The MACD is calculated by subtracting
        the long period EMA from the short period EMA. The result of that calculation is the
        MACD line. A signal line, which is an EMA of the MACD, is then calculated and can
        function as a trigger for buy and sell signals.

        :param stock_data: DataFrame containing stock data.
        :param short_window: Integer representing the short period EMA.
        :param long_window: Integer representing the long period EMA.
        :param signal_window: Integer representing the signal line EMA.
        :return: A tuple of two pd.Series, the first is the MACD line and the second is the Signal Line.
        """
        if not AdvancedFinancialIndicator.validate_data(stock_data, ['Close']):
            return None, None

        macd_series = (AdvancedFinancialIndicator.compute_ema(stock_data, short_window) -
                       AdvancedFinancialIndicator.compute_ema(stock_data, long_window))
        signal_line_series = macd_series.ewm(span=signal_window, adjust=False).mean()
        return macd_series, signal_line_series

    @staticmethod
    def compute_bollinger_bands(stock_data: pd.DataFrame, window: int = 20, num_std: int = 2,
                                column: str = 'Close') -> Tuple[Optional[pd.Series], Optional[pd.Series], Optional[pd.Series]]:
        """
        Compute Bollinger Bands.

        Bollinger Bands are a type of statistical chart characterizing the prices and
        volatility over time of a financial instrument or commodity. They consist of three
        bands: a middle band being an N-period simple moving average (SMA), an upper band
        at K times an N-period standard deviation above the middle band, and a lower band
        at K times an N-period standard deviation below the middle band. These bands help
        in identifying the overbought and oversold conditions in the market.

        :param stock_data: DataFrame containing stock data.
        :param window: Integer representing the moving average window size.
        :param num_std: Integer representing the number of standard deviations from the moving average.
        :param column: The column on which Bollinger Bands are to be computed.
        :return: A tuple of three pd.Series representing the Bollinger Upper, Middle, and Lower bands.
        """
        if not AdvancedFinancialIndicator.validate_data(stock_data, [column]):
            return None, None, None

        rolling_mean = stock_data[column].rolling(window=window).mean()
        rolling_std = stock_data[column].rolling(window=window).std()

        bollinger_upper_series = rolling_mean + (rolling_std * num_std)
        bollinger_mid_series = rolling_mean
        bollinger_lower_series = rolling_mean - (rolling_std * num_std)

        return bollinger_upper_series, bollinger_mid_series, bollinger_lower_series

    @staticmethod
    def compute_rsi(stock_data: pd.DataFrame, window: int = 14, column: str = 'Close') -> Optional[pd.Series]:
        """
        Compute Relative Strength Index (RSI).

        RSI is a momentum indicator that measures the magnitude of recent price changes
        to evaluate overbought or oversold conditions in the price of a stock or other asset.
        It is displayed as an oscillator (a line graph that moves between two extremes) and
        can have a reading from 0 to 100. The indicator was originally developed by J. Welles
        Wilder Jr. and introduced in his seminal 1978 book, "New Concepts in Technical Trading Systems."

        :param stock_data: DataFrame containing stock data.
        :param window: Integer representing the RSI calculation period.
        :param column: The column on which RSI is to be computed.
        :return: A pd.Series representing the RSI values, or None if validation fails.
        """
        if not AdvancedFinancialIndicator.validate_data(stock_data, [column]):
            return None

        delta = stock_data[column].diff()
        gain = (delta.clip(lower=0)).rolling(window=window).mean()
        loss = (-delta.clip(upper=0)).rolling(window=window).mean()
        rs = gain / loss
        rsi_series = 100 - (100 / (1 + rs))
        return rsi_series

    @staticmethod
    def compute_fibonacci_retracement(stock_data: pd.DataFrame, start_date_str: str, end_date_str: str) -> Dict[str, float]:
        """
        Compute Fibonacci Retracement Levels based on maximum high and minimum low in a date range.

        Fibonacci Retracement is a popular tool used by technical analysts to help identify strategic places
        for transactions, stop losses, or target prices to help traders get in at a good price. The Fibonacci
        levels are derived from the Fibonacci sequence, a set of numbers that starts with zero and one, with
        each subsequent number being the sum of the previous two. The key Fibonacci ratio of 61.8% - also
        referred to as "the golden ratio" or "the golden mean" - is found by dividing one number in the sequence
        by the number that follows it. Other key ratios include 38.2% and 23.6%.

        :param stock_data: DataFrame containing stock data.
        :param start_date: String representing the start date of the period.
        :param end_date: String representing the end date of the period.
        :return: Dictionary containing Fibonacci Retracement levels.
        """
        if 'Date' not in stock_data.columns:
            raise ValueError("DataFrame must contain a 'Date' column.")

        # Convert start_date and end_date to pandas Timestamp
        start_date = pd.to_datetime(start_date_str)
        end_date = pd.to_datetime(end_date_str)

        # Filter the DataFrame based on the date range without altering the index
        mask = (pd.to_datetime(stock_data['Date']) >= start_date) & (pd.to_datetime(stock_data['Date']) <= end_date)
        relevant_data = stock_data[mask]

        if relevant_data.empty:
            raise ValueError("No data found for the given date range.")

        high = relevant_data['High'].max()
        low = relevant_data['Low'].min()
        diff = high - low
        levels = {
            'Level_0': high,
            'Level_23.6%': high - diff * 0.236,
            'Level_38.2%': high - diff * 0.382,
            'Level_50%': high - diff * 0.5,
            'Level_61.8%': high - diff * 0.618,
            'Level_76.4%': high - diff * 0.764,
            'Level_100': low,
        }
        return levels

    @staticmethod
    def apply_strategy(stock_data: pd.DataFrame, short_window: int, long_window: int, volume_window: int,
                       column: str = 'Close') -> pd.DataFrame:
        """
        Apply a combined strategy on stock data incorporating MACD, Bollinger Bands, RSI, and Fibonacci Retracement.

        This function integrates various technical analysis indicators to create a holistic trading strategy.
        By combining indicators like MACD, Bollinger Bands, and RSI, the strategy aims to capture different
        aspects of the market's behavior, from trend following and momentum to volatility and potential
        support/resistance levels as indicated by Fibonacci Retracement. It is important to note that the
        effectiveness of any combined strategy can be subjective and should be validated with historical data
        to ensure reliability.

        :param stock_data: DataFrame with stock data.
        :param short_window: Window size for the short-term EMA.
        :param long_window: Window size for the long-term EMA.
        :param volume_window: Window size for volume averaging.
        :param column: The column on which to perform the analyses.
        :return: DataFrame with combined strategy signals.
        """
        if not AdvancedFinancialIndicator.validate_data(stock_data, [column, 'Volume']):
            return stock_data

        # Calculate indicators
        stock_data['MACD'], stock_data['Signal_Line'] = (
            AdvancedFinancialIndicator.compute_macd(stock_data, short_window, long_window))
        stock_data['Bollinger_Upper'], stock_data['Bollinger_Mid'], stock_data['Bollinger_Lower'] = (
            AdvancedFinancialIndicator.compute_bollinger_bands(stock_data, volume_window, column=column))
        stock_data['RSI'] = AdvancedFinancialIndicator.compute_rsi(stock_data, column=column)

        # Define signals based on combined indicators
        stock_data['Buy_Signal'] = ((stock_data['MACD'] > stock_data['Signal_Line']) &
                                    (stock_data['Close'] > stock_data['Bollinger_Lower']) &
                                    (stock_data['RSI'] < 70) &
                                    (stock_data['Volume'] > stock_data['Volume'].rolling(window=volume_window).mean()))

        stock_data['Sell_Signal'] = ((stock_data['MACD'] < stock_data['Signal_Line']) &
                                     (stock_data['Close'] < stock_data['Bollinger_Upper']) &
                                     (stock_data['RSI'] > 30))

        return stock_data

# Example usage:
# aapl_data = pd.read_csv('path_to_your_data.csv')
# analyzer = AdvancedFinancialIndicator()
# analyzed_data = analyzer.apply_strategy(aapl_data, short_window=12, long_window=26, volume_window=20)
# print(analyzed_data.tail())

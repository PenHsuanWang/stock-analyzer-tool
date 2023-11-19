
import pandas as pd


class PatternDefinitions:
    @staticmethod
    def is_bullish(open_price, close_price):
        return close_price > open_price

    @staticmethod
    def is_bearish(open_price, close_price):
        return close_price < open_price

    @staticmethod
    def is_doji(day):
        """Check if the candle is a doji."""
        # A doji's opening and closing prices should be nearly equal
        return abs(day['Open'] - day['Close']) <= (day['High'] - day['Low']) * 0.1  # or another small percentage

    @staticmethod
    def is_long_legged(day):
        """Check if the candle is a long-legged doji."""
        # A long-legged doji reflects indecision, so it should have a small body and long upper and lower shadows
        body_size = abs(day['Open'] - day['Close'])
        total_range = day['High'] - day['Low']
        return body_size <= total_range * 0.1  # or adjust the percentage as needed

    @staticmethod
    def is_gravestone(day):
        """Check if the candle is a gravestone doji."""
        # A gravestone doji should have a small body and a long upper shadow
        body_size = abs(day['Open'] - day['Close'])
        upper_shadow = day['High'] - max(day['Open'], day['Close'])
        return body_size <= (day['High'] - day['Low']) * 0.1 and upper_shadow >= body_size

    @staticmethod
    def is_dragonfly(day):
        """Check if the candle is a dragonfly doji."""
        # A dragonfly doji should have a small body and a long lower shadow
        body_size = abs(day['Open'] - day['Close'])
        lower_shadow = min(day['Open'], day['Close']) - day['Low']
        return body_size <= (day['High'] - day['Low']) * 0.1 and lower_shadow >= body_size

    @staticmethod
    def is_hammer(day):
        body = abs(day['Close'] - day['Open'])
        lower_shadow = day['Low'] - min(day['Open'], day['Close'])  # 修正此行

        return lower_shadow >= 2 * body and day['Open'] <= (day['High'] + day['Low']) / 2

    @staticmethod
    def is_inverse_hammer(day):
        body = abs(day['Close'] - day['Open'])
        upper_shadow = day['High'] - max(day['Open'], day['Close'])
        return upper_shadow > 2 * body and body < (day['High'] - day['Low']) / 3

    @staticmethod
    def is_bullish_engulfing(day, prev_day):
        return PatternDefinitions.is_bullish(day['Open'], day['Close']) and \
               PatternDefinitions.is_bearish(prev_day['Open'], prev_day['Close']) and \
               day['Open'] < prev_day['Close'] and day['Close'] > prev_day['Open']

    @staticmethod
    def is_piercing_line(day, prev_day):
        return PatternDefinitions.is_bearish(prev_day['Open'], prev_day['Close']) and \
               PatternDefinitions.is_bullish(day['Open'], day['Close']) and \
               day['Open'] < prev_day['Close'] and day['Close'] > (prev_day['Open'] + prev_day['Close']) / 2

    @staticmethod
    def is_morning_star(days):
        """Check if the 3-candle pattern is a morning star."""
        if len(days) != 3:
            return False

        first_candle = days.iloc[0]
        second_candle = days.iloc[1]
        third_candle = days.iloc[2]

        is_first_bearish = PatternDefinitions.is_bearish(first_candle['Open'], first_candle['Close'])
        is_third_bullish = PatternDefinitions.is_bullish(third_candle['Open'], third_candle['Close'])

        # Check if the second candle is a doji or a small body
        is_second_doji = PatternDefinitions.is_doji(second_candle)
        is_second_small_body = abs(second_candle['Open'] - second_candle['Close']) <= (
                first_candle['High'] - first_candle['Low']) * 0.1  # or another small percentage

        # The third candle's close should be at least halfway up the body of the first candle
        is_third_closing_in_first_body = third_candle['Close'] >= (first_candle['Open'] + first_candle['Close']) / 2

        return is_first_bearish and (
                    is_second_doji or is_second_small_body) and is_third_bullish and is_third_closing_in_first_body

    @staticmethod
    def is_three_white_soldiers(days):
        if len(days) != 3:
            return False

        return all(PatternDefinitions.is_bullish(row['Open'], row['Close']) for _, row in days.iterrows()) and \
            days.iloc[0]['Close'] < days.iloc[1]['Open'] < days.iloc[1]['Close'] < days.iloc[2]['Open']

    @staticmethod
    def is_hanging_man(day, prev_day):
        return PatternDefinitions.is_hammer(day) and \
               PatternDefinitions.is_bearish(day['Open'], day['Close']) and \
               prev_day['Close'] < day['Close']

    @staticmethod
    def is_shooting_star(day, prev_day):
        return PatternDefinitions.is_inverse_hammer(day) and \
               PatternDefinitions.is_bearish(day['Open'], day['Close']) and \
               prev_day['Close'] < day['Close']

    @staticmethod
    def is_bearish_engulfing(day, prev_day):
        return PatternDefinitions.is_bullish(prev_day['Open'], prev_day['Close']) and \
               PatternDefinitions.is_bearish(day['Open'], day['Close']) and \
               day['Open'] > prev_day['Close'] and day['Close'] < prev_day['Open']

    @staticmethod
    def is_evening_star(days):
        if len(days) != 3:
            return False

        return PatternDefinitions.is_bullish(days.iloc[0]['Open'], days.iloc[0]['Close']) and \
            min(days.iloc[1]['Open'], days.iloc[1]['Close']) < days.iloc[0]['Close'] and \
            PatternDefinitions.is_bearish(days.iloc[2]['Open'], days.iloc[2]['Close']) and \
            days.iloc[2]['Close'] < days.iloc[1]['Close']

    @staticmethod
    def is_three_black_crows(days):
        if len(days) != 3:
            return False

        return all(PatternDefinitions.is_bearish(row['Open'], row['Close']) for _, row in days.iterrows()) and \
            days.iloc[0]['Open'] > days.iloc[1]['Open'] > days.iloc[2]['Open']

    @staticmethod
    def is_dark_cloud_cover(day, prev_day):
        return PatternDefinitions.is_bullish(prev_day['Open'], prev_day['Close']) and \
               PatternDefinitions.is_bearish(day['Open'], day['Close']) and \
               day['Open'] > prev_day['Close'] and \
               day['Close'] < (prev_day['Open'] + prev_day['Close']) / 2


class PatternRecognizer:
    def __init__(self, data):
        self.data = data

    def recognize_patterns(self):
        self.data['Pattern'] = None
        for i in range(2, len(self.data)):
            day = self.data.iloc[i]
            prev_day = self.data.iloc[i - 1]
            prev_prev_day = self.data.iloc[i - 2]
            days = self.data.iloc[i - 2:i + 1]

            if PatternDefinitions.is_bullish_engulfing(day, prev_day):
                self.data.at[i, 'Pattern'] = 'Bullish Engulfing'
            elif PatternDefinitions.is_bearish_engulfing(day, prev_day):
                self.data.at[i, 'Pattern'] = 'Bearish Engulfing'
            elif PatternDefinitions.is_morning_star(days):
                self.data.at[i, 'Pattern'] = 'Morning Star'
            elif PatternDefinitions.is_evening_star(days):
                self.data.at[i, 'Pattern'] = 'Evening Star'
            elif PatternDefinitions.is_hammer(day):
                self.data.at[i, 'Pattern'] = 'Hammer'
            elif PatternDefinitions.is_inverse_hammer(day):
                self.data.at[i, 'Pattern'] = 'Inverse Hammer'
            elif PatternDefinitions.is_hanging_man(day, prev_day):
                self.data.at[i, 'Pattern'] = 'Hanging Man'
            elif PatternDefinitions.is_shooting_star(day, prev_day):
                self.data.at[i, 'Pattern'] = 'Shooting Star'
            elif PatternDefinitions.is_three_white_soldiers(days):
                self.data.at[i, 'Pattern'] = 'Three White Soldiers'
            elif PatternDefinitions.is_three_black_crows(days):
                self.data.at[i, 'Pattern'] = 'Three Black Crows'
            elif PatternDefinitions.is_dark_cloud_cover(day, prev_day):
                self.data.at[i, 'Pattern'] = 'Dark Cloud Cover'

        return self.data


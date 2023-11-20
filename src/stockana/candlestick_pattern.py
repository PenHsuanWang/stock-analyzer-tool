import pandas as pd


class PatternDefinitions:
    def __init__(self, doji_threshold=0.1, hammer_upper_shadow_multiplier=1):
        self.doji_threshold = doji_threshold
        self.hammer_upper_shadow_multiplier = hammer_upper_shadow_multiplier

    @staticmethod
    def _valid_candle(day):
        """Check if the candle data is valid."""
        return all(key in day for key in ['Open', 'Close', 'High', 'Low'])

    @staticmethod
    def _valid_candle_with_volume(day):
        """Check if the candle data is valid and includes volume."""
        return all(key in day for key in ['Open', 'Close', 'High', 'Low', 'Volume'])

    @staticmethod
    def is_higher_volume(day, prev_day):
        """Check if the volume is higher than the previous day."""
        return day['Volume'] > prev_day['Volume']

    # Example of integrating volume check in an existing method
    @staticmethod
    def is_bullish_engulfing_with_volume(day, prev_day):
        """Check if the pattern is a bullish engulfing with increased volume."""
        if not PatternDefinitions._valid_candle_with_volume(day) or not PatternDefinitions._valid_candle_with_volume(
                prev_day):
            return False
        return PatternDefinitions.is_bullish_engulfing(day, prev_day) and PatternDefinitions.is_higher_volume(day,
                                                                                                              prev_day)

    @staticmethod
    def is_bullish(open_price, close_price):
        """Check if the candle is bullish."""
        return close_price > open_price

    @staticmethod
    def is_bearish(open_price, close_price):
        """Check if the candle is bearish."""
        return close_price < open_price

    @staticmethod
    def is_doji(day, doji_threshold=0.1):
        """Check if the candle is a doji."""
        if not PatternDefinitions._valid_candle(day):
            return False
        return abs(day['Open'] - day['Close']) <= (day['High'] - day['Low']) * doji_threshold

    @staticmethod
    def is_long_legged(day, doji_threshold=0.1):
        """Check if the candle is a long-legged doji."""
        if not PatternDefinitions._valid_candle(day):
            return False
        body_size = abs(day['Open'] - day['Close'])
        total_range = day['High'] - day['Low']
        return body_size <= total_range * doji_threshold

    @staticmethod
    def is_gravestone(day, doji_threshold=0.1):
        """Check if the candle is a gravestone doji."""
        if not PatternDefinitions._valid_candle(day):
            return False
        body_size = abs(day['Open'] - day['Close'])
        upper_shadow = day['High'] - max(day['Open'], day['Close'])
        return body_size <= (day['High'] - day['Low']) * doji_threshold and upper_shadow >= body_size

    @staticmethod
    def is_dragonfly(day, doji_threshold=0.1):
        """Check if the candle is a dragonfly doji."""
        if not PatternDefinitions._valid_candle(day):
            return False
        body_size = abs(day['Open'] - day['Close'])
        lower_shadow = min(day['Open'], day['Close']) - day['Low']
        return body_size <= (day['High'] - day['Low']) * doji_threshold and lower_shadow >= body_size

    @staticmethod
    def is_hammer(day, is_downtrend, hammer_upper_shadow_multiplier=1):
        """Check if the candle is a hammer. Assumes it appears in a downtrend."""
        if not PatternDefinitions._valid_candle(day) or not is_downtrend:
            return False
        body = abs(day['Close'] - day['Open'])
        lower_shadow = min(day['Open'], day['Close']) - day['Low']
        upper_shadow = day['High'] - max(day['Open'], day['Close'])

        return lower_shadow >= 2 * body and upper_shadow <= body * hammer_upper_shadow_multiplier

    @staticmethod
    def is_inverse_hammer(day):
        """Check if the candle is an inverse hammer."""
        if not PatternDefinitions._valid_candle(day):
            return False
        body = abs(day['Close'] - day['Open'])
        upper_shadow = day['High'] - max(day['Open'], day['Close'])
        return upper_shadow >= 2 * body and body < (day['High'] - day['Low']) / 2

    @staticmethod
    def is_bullish_engulfing(day, prev_day):
        """Check if the pattern is a bullish engulfing."""
        if not all(key in day and key in prev_day for key in ['Open', 'Close']):
            return False
        return PatternDefinitions.is_bullish(day['Open'], day['Close']) and \
            PatternDefinitions.is_bearish(prev_day['Open'], prev_day['Close']) and \
            day['Open'] < prev_day['Close'] and day['Close'] > prev_day['Open']

    @staticmethod
    def is_piercing_line(day, prev_day):
        """Check if the pattern is a piercing line."""
        if not all(key in day and key in prev_day for key in ['Open', 'Close', 'High', 'Low']):
            return False
        return PatternDefinitions.is_bearish(prev_day['Open'], prev_day['Close']) and \
            PatternDefinitions.is_bullish(day['Open'], day['Close']) and \
            day['Open'] < prev_day['Close'] and \
            day['Close'] > (prev_day['Open'] + prev_day['Close']) / 2

    def is_morning_star(self, days):
        """Check if the 3-candle pattern is a morning star."""
        if len(days) != 3:
            return False
        if not all(all(key in day for key in ['Open', 'Close', 'High', 'Low']) for day in days):
            return False

        first_candle, second_candle, third_candle = days[0], days[1], days[2]

        is_first_bearish = PatternDefinitions.is_bearish(first_candle['Open'], first_candle['Close'])
        is_third_bullish = PatternDefinitions.is_bullish(third_candle['Open'], third_candle['Close'])

        is_second_doji = self.is_doji(second_candle)
        is_second_small_body = abs(second_candle['Open'] - second_candle['Close']) <= (
                first_candle['High'] - first_candle['Low']) * 0.1

        is_third_closing_in_first_body = third_candle['Close'] >= (first_candle['Open'] + first_candle['Close']) / 2

        return is_first_bearish and (is_second_doji or is_second_small_body) and \
            is_third_bullish and is_third_closing_in_first_body

    @staticmethod
    def is_three_white_soldiers(days):
        """Check if the pattern is three white soldiers."""
        if len(days) != 3:
            return False
        if not all(all(key in day for key in ['Open', 'Close']) for day in days):
            return False

        return all(PatternDefinitions.is_bullish(day['Open'], day['Close']) for day in days) and \
            days[0]['Close'] < days[1]['Open'] < days[1]['Close'] < days[2]['Open']

    @staticmethod
    def is_hanging_man(day, prev_day, is_uptrend):
        """Check if the pattern is a hanging man. Assumes it appears in an uptrend."""
        if not all(key in day and key in prev_day for key in ['Open', 'Close', 'High', 'Low']) or not is_uptrend:
            return False

        return PatternDefinitions.is_hammer(day, is_uptrend, hammer_upper_shadow_multiplier=3) and \
            day['Open'] < prev_day['Close']

    @staticmethod
    def is_shooting_star(day, prev_day, is_uptrend):
        """Check if the pattern is a shooting star. Assumes it appears in an uptrend."""
        if not all(key in day and key in prev_day for key in ['Open', 'Close', 'High', 'Low']) or not is_uptrend:
            return False
        return PatternDefinitions.is_inverse_hammer(day) and \
            day['Open'] < prev_day['Close']

    @staticmethod
    def is_bearish_engulfing(day, prev_day):
        """Check if the pattern is a bearish engulfing."""
        if not all(key in day and key in prev_day for key in ['Open', 'Close']):
            return False
        return PatternDefinitions.is_bearish(day['Open'], day['Close']) and \
            PatternDefinitions.is_bullish(prev_day['Open'], prev_day['Close']) and \
            day['Open'] > prev_day['Close'] and day['Close'] < prev_day['Open']

    @staticmethod
    def is_evening_star(days):
        """Check if the pattern is an evening star."""
        if len(days) != 3:
            return False
        if not all(all(key in day for key in ['Open', 'Close']) for day in days):
            return False

        return PatternDefinitions.is_bullish(days[0]['Open'], days[0]['Close']) and \
            min(days[1]['Open'], days[1]['Close']) < days[0]['Close'] and \
            PatternDefinitions.is_bearish(days[2]['Open'], days[2]['Close']) and \
            days[2]['Close'] < days[1]['Close']

    @staticmethod
    def is_three_black_crows(days):
        """Check if the pattern is three black crows."""
        if len(days) != 3:
            return False
        if not all(all(key in day for key in ['Open', 'Close']) for day in days):
            return False

        return all(PatternDefinitions.is_bearish(day['Open'], day['Close']) for day in days) and \
            days[0]['Open'] > days[1]['Open'] > days[2]['Open']

    @staticmethod
    def is_dark_cloud_cover(day, prev_day):
        """Check if the pattern is a dark cloud cover."""
        if not all(key in day and key in prev_day for key in ['Open', 'Close']):
            return False
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
            elif PatternDefinitions.is_bullish_engulfing_with_volume(day, prev_day):
                self.data.at[i, 'Pattern'] = 'Bullish Engulfing with Volume'

        return self.data
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
    def is_volume_increasing(day, prev_day):
        """Check if the volume is higher than the previous day."""
        return day['Volume'] > prev_day['Volume']

    @staticmethod
    def is_bullish(open_price, close_price):
        """Check if the candle is bullish."""
        return close_price > open_price

    @staticmethod
    def is_bearish(open_price, close_price):
        """Check if the candle is bearish."""
        return close_price < open_price

    @staticmethod
    def is_doji(day, doji_threshold=0.1, shadow_threshold=0.1):
        """
        Check if the candle is a doji.
        """
        if not PatternDefinitions._valid_candle(day):
            return False

        body_size = abs(day['Close'] - day['Open'])
        upper_shadow = day['High'] - max(day['Close'], day['Open'])
        lower_shadow = min(day['Close'], day['Open']) - day['Low']
        shadow_difference = abs(upper_shadow - lower_shadow)

        body_is_small = body_size <= (day['High'] - day['Low']) * doji_threshold
        shadows_are_approx_equal = shadow_difference <= (day['High'] - day['Low']) * shadow_threshold

        return body_is_small and shadows_are_approx_equal

    # Long-legged Doji check, where both shadows should be significantly long.
    @staticmethod
    def is_long_legged(day, doji_threshold=0.1, shadow_threshold=0.1):
        if not PatternDefinitions._valid_candle(day):
            return False
        body_size = abs(day['Open'] - day['Close'])
        upper_shadow = day['High'] - max(day['Open'], day['Close'])
        lower_shadow = min(day['Open'], day['Close']) - day['Low']
        shadow_difference = abs(upper_shadow - lower_shadow)

        body_is_small = body_size <= (day['High'] - day['Low']) * doji_threshold
        shadows_are_long = upper_shadow > body_size and lower_shadow > body_size
        shadows_are_approx_equal = shadow_difference <= (day['High'] - day['Low']) * shadow_threshold

        return body_is_small and shadows_are_long and shadows_are_approx_equal

    # Gravestone Doji check, where the upper shadow is significantly long and lower shadow is small or nonexistent.
    @staticmethod
    def is_gravestone(day, doji_threshold=0.1, shadow_threshold=0.1):
        if not PatternDefinitions._valid_candle(day):
            return False
        body_size = abs(day['Open'] - day['Close'])
        upper_shadow = day['High'] - max(day['Open'], day['Close'])
        lower_shadow = min(day['Open'], day['Close']) - day['Low']

        body_is_small = body_size <= (day['High'] - day['Low']) * doji_threshold
        upper_shadow_is_long = upper_shadow > body_size
        lower_shadow_is_small = lower_shadow <= body_size * shadow_threshold

        return body_is_small and upper_shadow_is_long and lower_shadow_is_small

    # Dragonfly Doji check, where the lower shadow is significantly long and upper shadow is small or nonexistent.
    @staticmethod
    def is_dragonfly(day, doji_threshold=0.1, shadow_threshold=0.1):
        if not PatternDefinitions._valid_candle(day):
            return False
        body_size = abs(day['Open'] - day['Close'])
        upper_shadow = day['High'] - max(day['Open'], day['Close'])
        lower_shadow = min(day['Open'], day['Close']) - day['Low']

        body_is_small = body_size <= (day['High'] - day['Low']) * doji_threshold
        lower_shadow_is_long = lower_shadow > body_size
        upper_shadow_is_small = upper_shadow <= body_size * shadow_threshold

        return body_is_small and lower_shadow_is_long and upper_shadow_is_small

    @staticmethod
    def is_hammer(day, is_downtrend, hammer_upper_shadow_multiplier=1):
        """
        Hammer at the end of a downtrend.
        """
        if not PatternDefinitions._valid_candle(day) or not is_downtrend:
            return False
        body = abs(day['Close'] - day['Open'])
        lower_shadow = min(day['Open'], day['Close']) - day['Low']
        upper_shadow = day['High'] - max(day['Open'], day['Close'])

        return lower_shadow >= 2 * body and upper_shadow <= body * hammer_upper_shadow_multiplier

    @staticmethod
    def is_inverse_hammer(day):
        """
        Inverse hammer geometry.
        """
        if not PatternDefinitions._valid_candle(day):
            return False
        body = abs(day['Close'] - day['Open'])
        upper_shadow = day['High'] - max(day['Open'], day['Close'])
        lower_shadow = min(day['Open'], day['Close']) - day['Low']
        total_length = day['High'] - day['Low']

        return upper_shadow >= 2 * body and body < total_length / 3 and lower_shadow < body

    @staticmethod
    def is_bullish_engulfing(day, prev_day):
        """
        Bullish Engulfing.
        """
        if not all(key in day and key in prev_day for key in ['Open', 'Close']):
            return False
        return PatternDefinitions.is_bullish(day['Open'], day['Close']) and \
            PatternDefinitions.is_bearish(prev_day['Open'], prev_day['Close']) and \
            day['Open'] < prev_day['Close'] and day['Close'] > prev_day['Open']

    @staticmethod
    def is_piercing_line(day, prev_day):
        """
        Piercing Line.
        """
        if not all(key in day and key in prev_day for key in ['Open', 'Close', 'High', 'Low']):
            return False
        return PatternDefinitions.is_bearish(prev_day['Open'], prev_day['Close']) and \
            PatternDefinitions.is_bullish(day['Open'], day['Close']) and \
            day['Open'] < prev_day['Close'] and \
            day['Close'] > (prev_day['Open'] + prev_day['Close']) / 2

    @staticmethod
    def is_morning_star(days):
        """
        Morning Star (3-candle bullish reversal).
        """
        if len(days) != 3:
            return False

        # Accept DataFrame or list
        if isinstance(days, pd.DataFrame):
            first_candle, second_candle, third_candle = days.iloc[0], days.iloc[1], days.iloc[2]
        else:
            first_candle, second_candle, third_candle = days[0], days[1], days[2]

        is_first_bearish = PatternDefinitions.is_bearish(first_candle['Open'], first_candle['Close'])
        is_third_bullish = PatternDefinitions.is_bullish(third_candle['Open'], third_candle['Close'])

        is_second_doji = PatternDefinitions.is_doji(second_candle)
        is_second_small_body = abs(second_candle['Open'] - second_candle['Close']) <= (
                first_candle['High'] - first_candle['Low']) * 0.1

        is_third_closing_in_first_body = third_candle['Close'] >= (first_candle['Open'] + first_candle['Close']) / 2

        return is_first_bearish and (is_second_doji or is_second_small_body) and \
            is_third_bullish and is_third_closing_in_first_body

    @staticmethod
    def is_three_white_soldiers(days):
        """
        Three White Soldiers — keep original simple rule, but accept list or DataFrame.
        """
        if len(days) != 3:
            return False

        # Accept DataFrame or list of dicts/Series
        if isinstance(days, pd.DataFrame):
            d0, d1, d2 = days.iloc[0], days.iloc[1], days.iloc[2]
        else:
            d0, d1, d2 = days[0], days[1], days[2]

        if not all(all(k in d for k in ['Open', 'Close']) for d in [d0, d1, d2]):
            return False

        return all(PatternDefinitions.is_bullish(d['Open'], d['Close']) for d in [d0, d1, d2]) and \
            d0['Close'] < d1['Open'] < d1['Close'] < d2['Open']

    @staticmethod
    def is_hanging_man(day, prev_day, is_uptrend):
        """
        Hanging Man in uptrend (original geometry reuse).
        """
        if not all(key in day and key in prev_day for key in ['Open', 'Close', 'High', 'Low']) or not is_uptrend:
            return False

        return PatternDefinitions.is_hammer(day, is_uptrend, hammer_upper_shadow_multiplier=3) and \
            day['Open'] < prev_day['Close']

    @staticmethod
    def is_shooting_star(day, prev_day, is_uptrend):
        """
        Shooting Star.
        """
        if not all(key in day and key in prev_day for key in ['Open', 'Close', 'High', 'Low']) or not is_uptrend:
            return False
        body = abs(day['Close'] - day['Open'])
        upper_shadow = day['High'] - max(day['Open'], day['Close'])
        return upper_shadow >= 2 * body and body < (day['High'] - day['Low']) / 2

    @staticmethod
    def is_bearish_engulfing(day, prev_day):
        """
        Bearish Engulfing.
        """
        if not all(key in day and key in prev_day for key in ['Open', 'Close']):
            return False
        return PatternDefinitions.is_bearish(day['Open'], day['Close']) and \
            PatternDefinitions.is_bullish(prev_day['Open'], prev_day['Close']) and \
            day['Open'] > prev_day['Close'] and day['Close'] < prev_day['Open']

    @staticmethod
    def is_evening_star(days):
        """
        Evening Star (3-candle bearish reversal).
        """
        if len(days) != 3:
            return False

        # Accept DataFrame or list
        if isinstance(days, pd.DataFrame):
            first_candle, second_candle, third_candle = days.iloc[0], days.iloc[1], days.iloc[2]
        else:
            first_candle, second_candle, third_candle = days[0], days[1], days[2]

        is_first_bullish = PatternDefinitions.is_bullish(first_candle['Open'], first_candle['Close'])
        is_third_bearish = PatternDefinitions.is_bearish(third_candle['Open'], third_candle['Close'])

        is_second_doji = PatternDefinitions.is_doji(second_candle)
        is_second_small_body = abs(second_candle['Open'] - second_candle['Close']) <= (
                first_candle['High'] - first_candle['Low']) * 0.1

        gap_up_from_first = second_candle['Low'] > first_candle['High']
        gap_down_to_third = second_candle['High'] < third_candle['Open']

        is_third_closing_below_midpoint_of_first = third_candle['Close'] < (
                    first_candle['Open'] + first_candle['Close']) / 2

        return is_first_bullish and (is_second_doji or is_second_small_body) and is_third_bearish and \
            gap_up_from_first and gap_down_to_third and is_third_closing_below_midpoint_of_first

    @staticmethod
    def is_three_black_crows(days):
        """
        Three Black Crows — keep original simple rule, but accept list or DataFrame.
        """
        if len(days) != 3:
            return False

        # Accept DataFrame or list of dicts/Series
        if isinstance(days, pd.DataFrame):
            d0, d1, d2 = days.iloc[0], days.iloc[1], days.iloc[2]
        else:
            d0, d1, d2 = days[0], days[1], days[2]

        if not all(all(k in d for k in ['Open', 'Close']) for d in [d0, d1, d2]):
            return False

        return all(PatternDefinitions.is_bearish(d['Open'], d['Close']) for d in [d0, d1, d2]) and \
            d0['Open'] > d1['Open'] > d2['Open']

    @staticmethod
    def is_dark_cloud_cover(day, prev_day):
        """
        Dark Cloud Cover.
        """
        if not all(key in day and key in prev_day for key in ['Open', 'Close']):
            return False
        midpoint = (prev_day['Open'] + prev_day['Close']) / 2
        return PatternDefinitions.is_bullish(prev_day['Open'], prev_day['Close']) and \
            PatternDefinitions.is_bearish(day['Open'], day['Close']) and \
            day['Open'] > prev_day['Close'] and \
            day['Close'] < midpoint

    @staticmethod
    def is_engulfing_with_volume(day, prev_day, pattern_type):
        """Check if the pattern is an engulfing pattern with increased volume."""
        if not PatternDefinitions._valid_candle_with_volume(day) or not PatternDefinitions._valid_candle_with_volume(prev_day):
            return False
        is_engulfing = (PatternDefinitions.is_bullish_engulfing(day, prev_day)
                        if pattern_type == 'bullish'
                        else PatternDefinitions.is_bearish_engulfing(day, prev_day))
        return is_engulfing and PatternDefinitions.is_volume_increasing(day, prev_day)

    @staticmethod
    def is_doji_with_volume(day, prev_day, doji_type, doji_threshold=0.1, shadow_threshold=0.1):
        """Check if the doji pattern occurs with increased volume."""
        if not PatternDefinitions._valid_candle_with_volume(day) or not PatternDefinitions._valid_candle_with_volume(prev_day):
            return False

        is_doji_type = False
        if doji_type == 'standard':
            is_doji_type = PatternDefinitions.is_doji(day, doji_threshold, shadow_threshold)
        elif doji_type == 'long_legged':
            is_doji_type = PatternDefinitions.is_long_legged(day, doji_threshold, shadow_threshold)
        elif doji_type == 'gravestone':
            is_doji_type = PatternDefinitions.is_gravestone(day, doji_threshold, shadow_threshold)
        elif doji_type == 'dragonfly':
            is_doji_type = PatternDefinitions.is_dragonfly(day, doji_threshold, shadow_threshold)

        return is_doji_type and PatternDefinitions.is_volume_increasing(day, prev_day)

    @staticmethod
    def is_hammer_with_volume(day, prev_day, is_downtrend, hammer_upper_shadow_multiplier=1):
        """Check if the candle is a hammer with increased volume. Assumes it appears in a downtrend."""
        if not PatternDefinitions._valid_candle_with_volume(day) or not PatternDefinitions._valid_candle_with_volume(prev_day) or not is_downtrend:
            return False
        is_hammer = PatternDefinitions.is_hammer(day, is_downtrend, hammer_upper_shadow_multiplier)
        return is_hammer and PatternDefinitions.is_volume_increasing(day, prev_day)

    @staticmethod
    def is_shooting_star_with_volume(day, prev_day, is_uptrend):
        """Check if the pattern is a shooting star with increased volume. Assumes it appears in an uptrend."""
        if not PatternDefinitions._valid_candle_with_volume(day) or not PatternDefinitions._valid_candle_with_volume(prev_day) or not is_uptrend:
            return False
        is_shooting_star = PatternDefinitions.is_shooting_star(day, prev_day, is_uptrend)
        return is_shooting_star and PatternDefinitions.is_volume_increasing(day, prev_day)


class PatternRecognizer:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def is_downtrend(self, index: int, lookback_period=5) -> bool:
        """
        Determine if there is a downtrend in the closing prices over a specified lookback period.
        (Use original monotonic logic to satisfy tests.)
        """
        if index < lookback_period:
            return False
        closing_prices = self.data['Close'][index - lookback_period:index]
        return closing_prices.is_monotonic_decreasing

    def is_uptrend(self, index: int, lookback_period=5) -> bool:
        """
        Determine if there is an uptrend in the closing prices over a specified lookback period.
        (Use original monotonic logic to satisfy tests.)
        """
        if index < lookback_period:
            return False
        closing_prices = self.data['Close'][index - lookback_period:index]
        return closing_prices.is_monotonic_increasing

    def recognize_patterns(self):
        self.data['Pattern'] = None
        for i in range(2, len(self.data)):
            day = self.data.iloc[i]
            prev_day = self.data.iloc[i - 1]
            days = self.data.iloc[i - 2:i + 1]

            date_index = day.name

            # Keep original ordering: plain patterns before volume-confirmed variants
            if PatternDefinitions.is_bullish_engulfing(day, prev_day):
                self.data.at[date_index, 'Pattern'] = 'Bullish Engulfing'
            elif PatternDefinitions.is_bearish_engulfing(day, prev_day):
                self.data.at[date_index, 'Pattern'] = 'Bearish Engulfing'
            elif PatternDefinitions.is_morning_star(days):
                self.data.at[date_index, 'Pattern'] = 'Morning Star'
            elif PatternDefinitions.is_evening_star(days):
                self.data.at[date_index, 'Pattern'] = 'Evening Star'
            elif PatternDefinitions.is_hammer(day, is_downtrend=self.is_downtrend(i)):
                self.data.at[date_index, 'Pattern'] = 'Hammer'
            elif PatternDefinitions.is_inverse_hammer(day):
                self.data.at[date_index, 'Pattern'] = 'Inverse Hammer'
            elif PatternDefinitions.is_hanging_man(day, prev_day, is_uptrend=self.is_uptrend(i)):
                self.data.at[date_index, 'Pattern'] = 'Hanging Man'
            elif PatternDefinitions.is_shooting_star(day, prev_day, is_uptrend=self.is_uptrend(i)):
                self.data.at[date_index, 'Pattern'] = 'Shooting Star'
            elif PatternDefinitions.is_three_white_soldiers(days):
                self.data.at[date_index, 'Pattern'] = 'Three White Soldiers'
            elif PatternDefinitions.is_three_black_crows(days):
                self.data.at[date_index, 'Pattern'] = 'Three Black Crows'
            elif PatternDefinitions.is_dark_cloud_cover(day, prev_day):
                self.data.at[date_index, 'Pattern'] = 'Dark Cloud Cover'
            elif PatternDefinitions.is_engulfing_with_volume(day, prev_day, 'bullish'):
                self.data.at[date_index, 'Pattern'] = 'Bullish Engulfing with Volume'
            elif PatternDefinitions.is_engulfing_with_volume(day, prev_day, 'bearish'):
                self.data.at[date_index, 'Pattern'] = 'Bearish Engulfing with Volume'
            elif PatternDefinitions.is_doji_with_volume(day, prev_day, 'standard'):
                self.data.at[date_index, 'Pattern'] = 'Doji with Volume'
            elif PatternDefinitions.is_hammer_with_volume(day, prev_day, is_downtrend=self.is_downtrend(i)):
                self.data.at[date_index, 'Pattern'] = 'Hammer with Volume'
            elif PatternDefinitions.is_shooting_star_with_volume(day, prev_day, is_uptrend=self.is_uptrend(i)):
                self.data.at[date_index, 'Pattern'] = 'Shooting Star with Volume'

        return self.data

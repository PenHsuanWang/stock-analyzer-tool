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
    def is_doji(day, doji_threshold=0.1):
        """
        Check if the candle is a doji. A doji is characterized by having a very small body,
        meaning the opening and closing prices are very close to each other. It indicates indecision
        or a struggle for turf positioning between buyers and sellers. Prices move above and below
        the opening level during the session, but close at or near the opening level.
        The 'doji_threshold' parameter defines how small the body should be relative to the range.
        """
        if not PatternDefinitions._valid_candle(day):
            return False
        return abs(day['Open'] - day['Close']) <= (day['High'] - day['Low']) * doji_threshold

    @staticmethod
    def is_long_legged(day, doji_threshold=0.1):
        """
        Check if the candle is a long-legged doji. This variant of a doji is where the
        upper and lower shadows are much longer than the regular doji, reflecting a great amount
        of indecision in the market. The 'doji_threshold' parameter is used to determine
        the size of the candle's body in comparison to its shadows.
        """
        if not PatternDefinitions._valid_candle(day):
            return False
        body_size = abs(day['Open'] - day['Close'])
        total_range = day['High'] - day['Low']
        return body_size <= total_range * doji_threshold

    @staticmethod
    def is_gravestone(day, doji_threshold=0.1):
        """
        Check if the candle is a gravestone doji. This pattern is identified by a small or
        nonexistent lower shadow and a long upper shadow, which suggests that the buying pressure
        was countered by strong selling pressure. This typically occurs at the end of an uptrend,
        signaling a bearish reversal. The 'doji_threshold' helps define the smallness of the body.
        """
        if not PatternDefinitions._valid_candle(day):
            return False
        body_size = abs(day['Open'] - day['Close'])
        upper_shadow = day['High'] - max(day['Open'], day['Close'])
        return body_size <= (day['High'] - day['Low']) * doji_threshold and upper_shadow >= body_size

    @staticmethod
    def is_dragonfly(day, doji_threshold=0.1):
        """
        Check if the candle is a dragonfly doji. This pattern has a long lower shadow and
        no upper shadow, with the opening and closing prices at or near the day's high.
        This pattern often signals a bullish reversal, especially when occurring after a downtrend.
        The 'doji_threshold' parameter determines the upper limit for the size of the candle's body.
        """
        if not PatternDefinitions._valid_candle(day):
            return False
        body_size = abs(day['Open'] - day['Close'])
        lower_shadow = min(day['Open'], day['Close']) - day['Low']
        return body_size <= (day['High'] - day['Low']) * doji_threshold and lower_shadow >= body_size

    @staticmethod
    def is_hammer(day, is_downtrend, hammer_upper_shadow_multiplier=1):
        """
        Check if the candle is a hammer. A hammer is identified by a small real body
        (the difference between the open and close prices) and a long lower shadow
        (indicating that the price has dropped significantly during the period but
        then partially recovered). This pattern is typically found at the bottom of a downtrend,
        signaling a potential bullish reversal. 'hammer_upper_shadow_multiplier' determines the
        maximum allowed size of the upper shadow relative to the body to qualify as a hammer.
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
        Check if the candle is an inverse hammer. An inverse hammer is characterized
        by a small real body and a long upper shadow, indicating that the price spiked
        higher during the period but then closed near the opening price. This pattern
        is generally found at the bottom of a downtrend and can signal a bullish reversal,
        especially when followed by further bullish confirmation.
        """
        if not PatternDefinitions._valid_candle(day):
            return False
        body = abs(day['Close'] - day['Open'])
        upper_shadow = day['High'] - max(day['Open'], day['Close'])
        lower_shadow = min(day['Open'], day['Close']) - day['Low']
        total_length = day['High'] - day['Low']

        # Check if the upper shadow is at least twice the body
        # and if the body is relatively small compared to the total length
        return upper_shadow >= 2 * body and body < total_length / 3 and lower_shadow < body

    @staticmethod
    def is_bullish_engulfing(day, prev_day):
        """
        Check if the pattern is a bullish engulfing. This pattern is characterized by a
        small bearish candle followed by a large bullish candle that completely 'engulfs'
        the body of the previous day's candle. This indicates a strong shift from selling
        to buying pressure and is considered a bullish reversal signal, especially when
        occurring after a downtrend.
        """
        if not all(key in day and key in prev_day for key in ['Open', 'Close']):
            return False
        return PatternDefinitions.is_bullish(day['Open'], day['Close']) and \
            PatternDefinitions.is_bearish(prev_day['Open'], prev_day['Close']) and \
            day['Open'] < prev_day['Close'] and day['Close'] > prev_day['Open']

    @staticmethod
    def is_piercing_line(day, prev_day):
        """
        Check if the pattern is a piercing line. This two-candle pattern starts with
        a strong bearish candle (signifying ongoing selling pressure) and is followed
        by a bullish candle which opens lower but closes within the body of the prior
        candle, ideally above the midpoint. This pattern suggests a potential bullish
        reversal, especially when it occurs in a downtrend.
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
        Check if the 3-candle pattern is a morning star. The morning star pattern is a
        bullish reversal pattern consisting of three candles: a strong bearish candle,
        a small-bodied candle (indicating indecision), and a strong bullish candle.
        This pattern indicates a shift in momentum from selling to buying. The middle
        candle can be a doji or a spinning top and should ideally gap away from the bodies
        of the adjacent candles.
        """
        if len(days) != 3:
            return False
        if not all(all(key in day for key in ['Open', 'Close', 'High', 'Low']) for day in days):
            return False

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
        Check if the pattern is three white soldiers. This pattern consists of three
        consecutive long-bodied bullish candles, each opening within the body of the
        previous candle and closing higher, signifying a strong upward trend. It suggests
        a shift from bearish to bullish sentiment and is especially significant after a
        period of price decline or consolidation.
        """
        if len(days) != 3:
            return False
        if not all(all(key in day for key in ['Open', 'Close']) for day in days):
            return False

        return all(PatternDefinitions.is_bullish(day['Open'], day['Close']) for day in days) and \
            days[0]['Close'] < days[1]['Open'] < days[1]['Close'] < days[2]['Open']

    @staticmethod
    def is_hanging_man(day, prev_day, is_uptrend):
        """
        Check if the pattern is a hanging man. The hanging man pattern is identified
        by a small body near the high with a little or no upper shadow and a long lower
        shadow. This pattern suggests that selling pressure is starting to outweigh buying
        pressure in an uptrend, potentially signaling the start of a bearish reversal.
        Its reliability is higher when it occurs after a sustained uptrend and is followed
        by bearish confirmation.
        """
        if not all(key in day and key in prev_day for key in ['Open', 'Close', 'High', 'Low']) or not is_uptrend:
            return False

        return PatternDefinitions.is_hammer(day, is_uptrend, hammer_upper_shadow_multiplier=3) and \
            day['Open'] < prev_day['Close']

    @staticmethod
    def is_shooting_star(day, prev_day, is_uptrend):
        """
        Check if the pattern is a shooting star. The shooting star is identified by a short body
        at the lower end of the trading range, with a long upper shadow. This pattern typically
        appears in an uptrend and suggests a potential bearish reversal. The long upper shadow
        indicates that the buyers initially pushed the prices up, but the sellers eventually
        drove them back down, closing near to the open. The reliability of this pattern is
        higher when it appears after a prolonged uptrend.
        """
        if not all(key in day and key in prev_day for key in ['Open', 'Close', 'High', 'Low']) or not is_uptrend:
            return False
        body = abs(day['Close'] - day['Open'])
        upper_shadow = day['High'] - max(day['Open'], day['Close'])
        return upper_shadow >= 2 * body and body < (day['High'] - day['Low']) / 2

    @staticmethod
    def is_bearish_engulfing(day, prev_day):
        """
        Check if the pattern is a bearish engulfing. This pattern is formed when a small bullish
        candle is followed by a large bearish candle that completely engulfs the body of the
        previous day's candle. It indicates a shift from buying to selling pressure and is
        considered a bearish reversal signal, especially when occurring after an uptrend.
        """
        if not all(key in day and key in prev_day for key in ['Open', 'Close']):
            return False
        return PatternDefinitions.is_bearish(day['Open'], day['Close']) and \
            PatternDefinitions.is_bullish(prev_day['Open'], prev_day['Close']) and \
            day['Open'] > prev_day['Close'] and day['Close'] < prev_day['Open']

    @staticmethod
    def is_evening_star(days):
        """
        Check if the pattern is an evening star. The evening star is a three-candle bearish
        reversal pattern consisting of a large bullish candle, a small-bodied candle, and a
        large bearish candle. It reflects a shift in momentum from buying to selling.
        The pattern is more reliable when it appears after a strong uptrend and the middle
        candle gaps above the first and below the third.
        """
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
        """
        Check if the pattern is three black crows. This pattern consists of three consecutive
        long-bodied bearish candles that open within the body of the previous candle and
        close lower than the previous candle. It indicates a strong bearish sentiment and
        is typically seen as a bearish reversal signal, particularly when occurring after an
        uptrend.
        """
        if len(days) != 3:
            return False
        if not all(all(key in day for key in ['Open', 'Close']) for day in days):
            return False

        return all(PatternDefinitions.is_bearish(day['Open'], day['Close']) for day in days) and \
            days[0]['Open'] > days[1]['Open'] > days[2]['Open']

    @staticmethod
    def is_dark_cloud_cover(day, prev_day):
        """
        Check if the pattern is a dark cloud cover. This bearish reversal pattern is identified
        by a bullish candle followed by a bearish candle that opens above the high of the previous
        day and closes below the midpoint of the body of the previous day's candle. It suggests
        that the bulls initially continued to push the price higher, but the bears ultimately gained
        control and pushed the price down, signaling a potential trend reversal.
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
        if not PatternDefinitions._valid_candle_with_volume(day) or not PatternDefinitions._valid_candle_with_volume(
                prev_day):
            return False
        is_engulfing = (PatternDefinitions.is_bullish_engulfing(day,
                                                                prev_day) if pattern_type == 'bullish' else PatternDefinitions.is_bearish_engulfing(
            day, prev_day))
        return is_engulfing and PatternDefinitions.is_volume_increasing(day, prev_day)

    @staticmethod
    def is_doji_with_volume(day, prev_day, doji_type):
        """Check if the doji pattern occurs with increased volume."""
        if not PatternDefinitions._valid_candle_with_volume(day) or not PatternDefinitions._valid_candle_with_volume(
                prev_day):
            return False
        is_doji_type = (PatternDefinitions.is_doji(day) if doji_type == 'standard' else
                        PatternDefinitions.is_long_legged(day) if doji_type == 'long_legged' else
                        PatternDefinitions.is_gravestone(day) if doji_type == 'gravestone' else
                        PatternDefinitions.is_dragonfly(day) if doji_type == 'dragonfly' else False)
        return is_doji_type and PatternDefinitions.is_volume_increasing(day, prev_day)

    @staticmethod
    def is_hammer_with_volume(day, prev_day, is_downtrend, hammer_upper_shadow_multiplier=1):
        """Check if the candle is a hammer with increased volume. Assumes it appears in a downtrend."""
        if not PatternDefinitions._valid_candle_with_volume(day) or not PatternDefinitions._valid_candle_with_volume(
                prev_day) or not is_downtrend:
            return False
        is_hammer = PatternDefinitions.is_hammer(day, is_downtrend, hammer_upper_shadow_multiplier)
        return is_hammer and PatternDefinitions.is_volume_increasing(day, prev_day)

    @staticmethod
    def is_shooting_star_with_volume(day, prev_day, is_uptrend):
        """Check if the pattern is a shooting star with increased volume. Assumes it appears in an uptrend."""
        if not PatternDefinitions._valid_candle_with_volume(day) or not PatternDefinitions._valid_candle_with_volume(
                prev_day) or not is_uptrend:
            return False
        is_shooting_star = PatternDefinitions.is_shooting_star(day, prev_day, is_uptrend)
        return is_shooting_star and PatternDefinitions.is_volume_increasing(day, prev_day)


class PatternRecognizer:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def is_downtrend(self, index: int, lookback_period=5) -> bool:
        """
        Determine if there is a downtrend in the closing prices over a specified lookback period.

        :param data: DataFrame containing stock data with 'Close' prices.
        :param index: Current index in the DataFrame to check for a downtrend.
        :param lookback_period: Number of days to look back to check for a downtrend.
        :return: True if there is a downtrend, False otherwise.
        """
        if index < lookback_period:
            # Not enough data to determine a trend
            return False

        closing_prices = self.data['Close'][index - lookback_period:index]
        return closing_prices.is_monotonic_decreasing

    def is_uptrend(self, index: int, lookback_period=5) -> bool:
        """
        Determine if there is an uptrend in the closing prices over a specified lookback period.

        :param index: Current index in the DataFrame to check for an uptrend.
        :param lookback_period: Number of days to look back to check for an uptrend.
        :return: True if there is an uptrend, False otherwise.
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

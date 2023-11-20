import pytest
import os

from src.stockana.candlestick_pattern import PatternDefinitions


def create_day(open_price, high_price, low_price, close_price, volume=0):
    return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price, 'Volume': volume}


class TestPatternDefinitions:
    @pytest.fixture
    def pattern_definitions(self):
        return PatternDefinitions()

    def test_is_bullish(self):
        assert PatternDefinitions.is_bullish(100, 110) == True
        assert PatternDefinitions.is_bullish(110, 100) == False

    def test_is_bearish(self):
        assert PatternDefinitions.is_bearish(110, 100) == True
        assert PatternDefinitions.is_bearish(100, 110) == False

    def test_is_doji(self, pattern_definitions):
        day = create_day(100, 105, 95, 100.05)
        assert pattern_definitions.is_doji(day)

        day = create_day(100, 105, 95, 103)
        assert not pattern_definitions.is_doji(day)

    def test_is_hammer(self, pattern_definitions):
        # Correct hammer pattern
        day = create_day(100, 102, 90, 98)  # Ensure lower shadow is twice the body and upper shadow meets the criteria
        assert pattern_definitions.is_hammer(day, is_downtrend=True)

        # Hammer in uptrend (should return False)
        assert not pattern_definitions.is_hammer(day, is_downtrend=False)

        # Incorrect shape for a hammer
        day = create_day(100, 108, 99, 107)  # Ensure this does not meet hammer criteria
        assert not pattern_definitions.is_hammer(day, is_downtrend=True)

    def test_is_inverse_hammer(self, pattern_definitions):
        # Inverse Hammer
        day = create_day(100, 110, 99.5, 101)
        assert pattern_definitions.is_inverse_hammer(day)

        # Not an inverse hammer due to inappropriate shape
        day = create_day(100, 105, 95, 103)
        assert not pattern_definitions.is_inverse_hammer(day)

    def test_is_bullish_engulfing(self):
        prev_day = create_day(100, 105, 95, 98)
        day = create_day(97, 110, 96, 109)
        assert PatternDefinitions.is_bullish_engulfing(day, prev_day)

        # Not a bullish engulfing pattern
        day = create_day(97, 105, 96, 99)
        assert not PatternDefinitions.is_bullish_engulfing(day, prev_day)

    def test_is_bullish_engulfing_with_volume(self, pattern_definitions):
        prev_day = create_day(100, 105, 95, 98, 1000)
        day = create_day(97, 110, 96, 109, 1500)
        assert PatternDefinitions.is_bullish_engulfing_with_volume(day, prev_day)

        day['Volume'] = 800  # Lower volume than previous day
        assert not PatternDefinitions.is_bullish_engulfing_with_volume(day, prev_day)

    def test_is_piercing_line(self):
        prev_day = create_day(100, 105, 90, 92)
        day = create_day(91, 102, 90, 101)
        assert PatternDefinitions.is_piercing_line(day, prev_day)

        # Not a piercing line pattern
        day = create_day(91, 99, 90, 95)
        assert not PatternDefinitions.is_piercing_line(day, prev_day)

    def test_is_morning_star(self, pattern_definitions):
        day1 = create_day(100, 105, 95, 96)
        day2 = create_day(95, 97, 94, 95.5)
        day3 = create_day(96, 105, 95, 104)
        days = [day1, day2, day3]
        assert pattern_definitions.is_morning_star(days) == True

        day3['Close'] = 95  # Third day does not close in the body of the first day
        assert pattern_definitions.is_morning_star(days) == False

    def test_is_three_white_soldiers(self):
        day1 = create_day(100, 105, 99, 104)
        day2 = create_day(105, 109, 103, 108)
        day3 = create_day(109, 113, 107, 112)
        days = [day1, day2, day3]
        assert PatternDefinitions.is_three_white_soldiers(days)

        # Not three white soldiers
        day3 = create_day(108, 110, 107, 109)  # Smaller candle
        days = [day1, day2, day3]
        assert not PatternDefinitions.is_three_white_soldiers(days)

    def test_is_hanging_man(self):
        prev_day = create_day(100, 105, 95, 102)  # Uptrend context
        day = create_day(101, 102, 96, 100)  # Potential Hanging Man pattern
        assert PatternDefinitions.is_hanging_man(day, prev_day, is_uptrend=True)

        assert not PatternDefinitions.is_hanging_man(day, prev_day, is_uptrend=False)  # Not in an uptrend

        # Adjust test data to clearly not meet Hanging Man criteria
        day_not_hanging_man = create_day(104, 108, 102, 106)  # Lower shadow not long enough
        assert not PatternDefinitions.is_hanging_man(day_not_hanging_man, prev_day, is_uptrend=True)

    def test_is_shooting_star(self):
        # Shooting Star in an uptrend
        prev_day = create_day(100, 105, 95, 104)
        day = create_day(104, 112, 103, 105)  # Long upper shadow, small body
        assert PatternDefinitions.is_shooting_star(day, prev_day, is_uptrend=True)

        # Not a Shooting Star due to downtrend
        assert not PatternDefinitions.is_shooting_star(day, prev_day, is_uptrend=False)

        # Not a Shooting Star due to inappropriate shape (small upper shadow)
        day = create_day(104, 105, 99, 103)
        assert not PatternDefinitions.is_shooting_star(day, prev_day, is_uptrend=True)

    def test_is_bearish_engulfing(self):
        prev_day = create_day(100, 105, 95, 104)  # Bullish candle
        day = create_day(105, 110, 100, 99)  # Bearish Engulfing pattern
        assert PatternDefinitions.is_bearish_engulfing(day, prev_day)

        # Not a bearish engulfing pattern
        day = create_day(102, 106, 101, 103)
        assert not PatternDefinitions.is_bearish_engulfing(day, prev_day)

    def test_is_evening_star(self):
        day1 = create_day(100, 105, 99, 104)  # Bullish candle
        day2 = create_day(105, 106, 104, 105.5)  # Small body candle
        day3 = create_day(105, 106, 100, 101)  # Bearish candle
        days = [day1, day2, day3]
        assert PatternDefinitions.is_evening_star(days)

        # Not an evening star pattern
        day3 = create_day(105, 110, 104, 109)
        days = [day1, day2, day3]
        assert not PatternDefinitions.is_evening_star(days)

    def test_is_three_black_crows(self):
        day1 = create_day(100, 100, 95, 96)  # Bearish candle
        day2 = create_day(96, 96, 90, 91)  # Bearish candle
        day3 = create_day(91, 91, 85, 86)  # Bearish candle
        days = [day1, day2, day3]
        assert PatternDefinitions.is_three_black_crows(days)

        # Not three black crows pattern
        day3 = create_day(91, 95, 90, 94)
        days = [day1, day2, day3]
        assert not PatternDefinitions.is_three_black_crows(days)

    def test_is_dark_cloud_cover(self):
        prev_day = create_day(100, 105, 95, 104)  # Bullish candle
        day = create_day(105, 110, 100, 102)  # Opens above prev close, closes below midpoint
        assert PatternDefinitions.is_dark_cloud_cover(day, prev_day)

        # Not a Dark Cloud Cover (does not close below midpoint)
        day = create_day(105, 110, 100, 103)
        assert not PatternDefinitions.is_dark_cloud_cover(day, prev_day)

        # Not a Dark Cloud Cover (previous day is bearish)
        prev_day = create_day(100, 105, 95, 96)
        assert not PatternDefinitions.is_dark_cloud_cover(day, prev_day)


if __name__ == "__main__":
    print(os.getcwd())
    pytest.main()

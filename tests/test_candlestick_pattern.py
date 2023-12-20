import pytest
import os
import pandas as pd

from src.stockana.candlestick_pattern import PatternDefinitions, PatternRecognizer


def create_day(open_price, high_price, low_price, close_price, volume=0):
    return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price, 'Volume': volume}


class TestPatternDefinitions:
    @pytest.fixture
    def pattern_definitions(self):
        return PatternDefinitions()

    def test_is_volume_increasing(self):
        assert PatternDefinitions.is_volume_increasing({'Volume': 200}, {'Volume': 100}) == True
        assert PatternDefinitions.is_volume_increasing({'Volume': 100}, {'Volume': 200}) == False
        assert PatternDefinitions.is_volume_increasing({'Volume': 100}, {'Volume': 100}) == False

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

    def test_is_hammer_invalid_candle(self, pattern_definitions):
        # Test with an invalid candle (missing keys)
        day = {'Open': 100, 'Close': 98, 'Low': 90}  # Missing 'High' key
        assert not pattern_definitions.is_hammer(day, is_downtrend=True)

    def test_is_inverse_hammer_invalid_candle(self, pattern_definitions):
        day = {'Open': 100, 'Close': 102, 'Low': 98}  # Missing 'High' key
        assert not pattern_definitions.is_inverse_hammer(day)

    def test_is_bullish_engulfing(self):
        prev_day = create_day(100, 105, 95, 98)
        day = create_day(97, 110, 96, 109)
        assert PatternDefinitions.is_bullish_engulfing(day, prev_day)

        # Not a bullish engulfing pattern
        day = create_day(97, 105, 96, 99)
        assert not PatternDefinitions.is_bullish_engulfing(day, prev_day)

    def test_is_piercing_line(self):
        prev_day = create_day(100, 105, 90, 92)
        day = create_day(91, 102, 90, 101)
        assert PatternDefinitions.is_piercing_line(day, prev_day)

        # Not a piercing line pattern
        day = create_day(91, 99, 90, 95)
        assert not PatternDefinitions.is_piercing_line(day, prev_day)

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
        day = create_day(105, 110, 100, 101.5)  # Opens above prev close, closes below midpoint
        assert PatternDefinitions.is_dark_cloud_cover(day, prev_day)

        # Not a Dark Cloud Cover (does not close below midpoint)
        day = create_day(105, 110, 100, 103)
        assert not PatternDefinitions.is_dark_cloud_cover(day, prev_day)

        # Not a Dark Cloud Cover (previous day is bearish)
        prev_day = create_day(100, 105, 95, 96)
        assert not PatternDefinitions.is_dark_cloud_cover(day, prev_day)

    def test_is_engulfing_with_volume(self, pattern_definitions):
        prev_day = create_day(100, 105, 95, 98, 1000)
        day = create_day(97, 110, 96, 109, 1500)
        assert pattern_definitions.is_engulfing_with_volume(day, prev_day, 'bullish')

        day['Volume'] = 800  # Lower volume than previous day
        assert not pattern_definitions.is_engulfing_with_volume(day, prev_day, 'bullish')

        # test for bearish
        prev_day = create_day(100, 105, 95, 102, 1000)
        day = create_day(103, 106, 94, 96, 1500)
        assert pattern_definitions.is_engulfing_with_volume(day, prev_day, 'bearish')

        day['Volume'] = 800  # Lower volume than previous day
        assert not pattern_definitions.is_engulfing_with_volume(day, prev_day, 'bearish')

    def test_is_doji_with_volume(self, pattern_definitions):
        prev_day = create_day(100, 105, 100, 102, 1000)
        day = create_day(102, 103, 101, 102, 1500)  # Doji with small body
        assert pattern_definitions.is_doji_with_volume(day, prev_day, 'standard')

        day['Volume'] = 800
        assert not pattern_definitions.is_doji_with_volume(day, prev_day, 'standard')

    def test_is_hammer_with_volume(self, pattern_definitions):
        prev_day = create_day(105, 110, 104, 106, 1000)
        day = create_day(102, 103, 90, 100, 1500)  # Hammer in downtrend
        assert pattern_definitions.is_hammer_with_volume(day, prev_day, is_downtrend=True)

        day['Volume'] = 800
        assert not pattern_definitions.is_hammer_with_volume(day, prev_day, is_downtrend=True)

    def test_is_shooting_star_with_volume(self, pattern_definitions):
        prev_day = create_day(95, 100, 94, 98, 1000)
        day = create_day(99, 108, 98, 100, 1500)  # Shooting Star in uptrend
        assert pattern_definitions.is_shooting_star_with_volume(day, prev_day, is_uptrend=True)

        day['Volume'] = 800
        assert not pattern_definitions.is_shooting_star_with_volume(day, prev_day, is_uptrend=True)

    def test_is_long_legged_doji(self, pattern_definitions):
        # Long-legged Doji
        day = create_day(100, 110, 90, 100.05)
        assert pattern_definitions.is_long_legged(day)

        # Not a long-legged Doji due to large body
        day = create_day(100, 110, 90, 105)
        assert not pattern_definitions.is_long_legged(day)

    def test_is_gravestone_doji(self, pattern_definitions):
        # Gravestone Doji
        day = create_day(100, 110, 100, 100)
        assert pattern_definitions.is_gravestone(day)

        # Not a gravestone Doji
        day = create_day(100, 110, 90, 105)
        assert not pattern_definitions.is_gravestone(day)

    def test_is_dragonfly_doji(self, pattern_definitions):
        # Dragonfly Doji
        day = create_day(100, 100, 90, 100)
        assert pattern_definitions.is_dragonfly(day)

        # Not a dragonfly Doji
        day = create_day(100, 110, 90, 110)
        assert not pattern_definitions.is_dragonfly(day)

    def test_is_downtrend(self):
        data = pd.DataFrame({'Close': [100, 98, 96, 94, 92]})
        pattern_recognizer = PatternRecognizer(data)
        assert pattern_recognizer.is_downtrend(4, 3)

        data = pd.DataFrame({'Close': [100, 102, 104, 106, 108]})
        pattern_recognizer = PatternRecognizer(data)
        assert not pattern_recognizer.is_downtrend(4, 3)

    def test_is_uptrend(self):
        data = pd.DataFrame({'Close': [100, 102, 104, 106, 108]})
        pattern_recognizer = PatternRecognizer(data)
        assert pattern_recognizer.is_uptrend(4, 3) == True

        data = pd.DataFrame({'Close': [100, 98, 96, 94, 92]})
        pattern_recognizer = PatternRecognizer(data)
        assert pattern_recognizer.is_uptrend(4, 3) == False


    def test_recognize_bullish_engulfing(self):
        data = pd.DataFrame({
            'Open': [100, 95, 90, 85, 79],
            'High': [105, 100, 95, 90, 87],
            'Low': [95, 90, 85, 80, 80],
            'Close': [96, 91, 86, 82, 91],  # Day 5 forms a Bullish Engulfing pattern with Day 4
            'Volume': [1000, 1100, 1200, 1300, 1400]
        })
        pattern_recognizer = PatternRecognizer(data)
        recognized_patterns = pattern_recognizer.recognize_patterns()

        # Adjust this assertion based on the expected recognized pattern
        assert recognized_patterns['Pattern'].iloc[-1] == 'Bullish Engulfing'

    def test_recognize_bearish_engulfing(self):
        data_bearish_engulfing = pd.DataFrame({
            'Open': [100, 105, 110, 115, 120],
            'High': [105, 110, 115, 120, 119],
            'Low': [99, 104, 109, 113, 112],
            'Close': [104, 109, 114, 119, 113],  # Day 5 forms a Bearish Engulfing pattern with Day 4
            'Volume': [1000, 1200, 1400, 1600, 1800]
        })

        pattern_recognizer = PatternRecognizer(data_bearish_engulfing)
        recognized_patterns = pattern_recognizer.recognize_patterns()

        assert recognized_patterns['Pattern'].iloc[-1] == 'Bearish Engulfing'

        # Add more assertions based on expected patterns

    def test_recognize_hammer(self):
        data_hammer = pd.DataFrame({
            'Open': [102, 101, 100, 98, 95, 92, 89],
            'High': [103, 102, 101, 99, 96, 93, 91],
            'Low': [97, 96, 95, 93, 90, 87, 80],
            'Close': [101, 100, 99, 97, 94, 91, 90],
            'Volume': [900, 950, 1000, 1050, 1100, 1150, 1200]
        })

        pattern_recognizer = PatternRecognizer(data_hammer)
        recognized_patterns = pattern_recognizer.recognize_patterns()

        assert recognized_patterns['Pattern'].iloc[-1] == 'Hammer'

    def test_recognize_shooting_star(self):
        data_shooting_star = pd.DataFrame({
            'Open': [98, 100, 102, 104, 106, 108, 110],
            'High': [99, 101, 103, 105, 110, 112, 114],  # Day 7 forms a Shooting Star
            'Low': [97, 99, 101, 103, 105, 108, 108],
            'Close': [99, 101, 103, 105, 109, 110, 111],
            'Volume': [900, 1000, 1100, 1200, 1300, 1400, 1500]
        })

        pattern_recognizer = PatternRecognizer(data_shooting_star)
        recognized_patterns = pattern_recognizer.recognize_patterns()

        assert recognized_patterns['Pattern'].iloc[-1] == 'Shooting Star'

    def test_recognize_doji_with_volume(self):
        data_doji = pd.DataFrame({
            'Open': [100, 102, 104, 106, 108],
            'High': [101, 103, 105, 107, 110],
            'Low': [99, 101, 103, 105, 106],
            'Close': [100, 102, 104, 106, 108],  # Day 5 forms a Doji
            'Volume': [1000, 1100, 1200, 1300, 1400]
        })

        pattern_recognizer = PatternRecognizer(data_doji)
        recognized_patterns = pattern_recognizer.recognize_patterns()

        assert recognized_patterns['Pattern'].iloc[-1] == 'Doji with Volume'

    def test_recognize_inverted_hammer(self):
        data_inverted_hammer = pd.DataFrame({
            'Open': [100, 98, 96, 94, 92],
            'High': [100, 98, 96, 97, 99],  # Day 5 forms an Inverted Hammer
            'Low': [95, 93, 91, 90, 91.9],
            'Close': [96, 94, 92, 91, 93],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        })

        pattern_recognizer = PatternRecognizer(data_inverted_hammer)
        recognized_patterns = pattern_recognizer.recognize_patterns()

        assert recognized_patterns['Pattern'].iloc[-1] == 'Inverse Hammer'

    def test_recognize_hanging_man(self):
        data_hanging_man = pd.DataFrame({
            'Open': [100, 102, 104, 106, 108, 110, 111.1],
            'High': [101, 103, 105, 107, 109, 111.3, 111.2],
            'Low': [99, 101, 103, 105, 107, 108, 107],
            'Close': [101, 103, 105, 107, 109, 111.2, 111],
            'Volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600]
        })

        pattern_recognizer = PatternRecognizer(data_hanging_man)
        recognized_patterns = pattern_recognizer.recognize_patterns()

        assert recognized_patterns['Pattern'].iloc[-1] == 'Hanging Man'

    def test_recognize_morning_star(self):
        data_morning_star = pd.DataFrame({
            'Open': [102, 103, 100, 98, 99],
            'High': [106, 107, 105, 102, 103],
            'Low': [99, 102, 95, 94, 98],
            'Close': [104, 105, 96, 98, 102],
            'Volume': [800, 900, 1000, 500, 1500]
        })

        pattern_recognizer = PatternRecognizer(data_morning_star)
        recognized_patterns = pattern_recognizer.recognize_patterns()

        # As the Morning Star pattern spans 3 days, check the pattern of the last day of the pattern
        assert recognized_patterns['Pattern'].iloc[-1] == 'Morning Star'


if __name__ == "__main__":
    print(os.getcwd())
    pytest.main()

import pytest
import pandas as pd

from src.stockana.candlestick_pattern import PatternDefinitions

def create_day(open_price, high_price, low_price, close_price):
    return {'Open': open_price, 'High': high_price, 'Low': low_price, 'Close': close_price}


class TestPatternDefinitions:
    def test_is_bullish(self):
        assert PatternDefinitions.is_bullish(100, 110) == True
        assert PatternDefinitions.is_bullish(110, 100) == False

    def test_is_bearish(self):
        assert PatternDefinitions.is_bearish(110, 100) == True
        assert PatternDefinitions.is_bearish(100, 110) == False

    def test_is_hammer(self):
        hammer = create_day(100, 110, 90, 102)  # Long lower shadow, short body
        not_hammer = create_day(100, 110, 99, 105)  # Short lower shadow
        assert PatternDefinitions.is_hammer(hammer) == True
        assert PatternDefinitions.is_hammer(not_hammer) == False

    def test_is_inverse_hammer(self):
        inverse_hammer = create_day(100, 115, 100, 102)  # Long upper shadow, short body
        not_inverse_hammer = create_day(100, 102, 95, 101)  # Short upper shadow
        assert PatternDefinitions.is_inverse_hammer(inverse_hammer) == True
        assert PatternDefinitions.is_inverse_hammer(not_inverse_hammer) == False

    def test_is_bullish_engulfing(self):
        day1 = create_day(105, 106, 100, 101)
        day2 = create_day(100, 110, 99, 109)
        assert PatternDefinitions.is_bullish_engulfing(day2, day1) == True

        day1 = create_day(100, 105, 99, 104)
        day2 = create_day(105, 110, 104, 106)
        assert PatternDefinitions.is_bullish_engulfing(day2, day1) == False

    def test_is_piercing_line(self):
        day1 = create_day(105, 106, 100, 101)
        day2 = create_day(100, 106, 99, 104)  # Second day closes above the midpoint of the first day
        assert PatternDefinitions.is_piercing_line(day2, day1) == True

        day2 = create_day(100, 104, 99, 102)  # Second day does not close above the midpoint
        assert PatternDefinitions.is_piercing_line(day2, day1) == False

    def test_is_morning_star(self):
        day1 = create_day(105, 106, 100, 101)  # Bearish
        day2 = create_day(101, 105, 97, 101)  # Small body
        day3 = create_day(101, 110, 100, 109)  # Bullish, closes above day 2 close
        days = pd.DataFrame([day1, day2, day3])
        assert PatternDefinitions.is_morning_star(days) == True

        day3 = create_day(101, 105, 101, 100)  # Does not close above the midpoint of the first day
        days = pd.DataFrame([day1, day2, day3])
        assert PatternDefinitions.is_morning_star(days) == False

    def test_is_three_white_soldiers(self):
        day1 = create_day(100, 105, 99, 104)
        day2 = create_day(105, 110, 104, 109)  # Open at or above the previous close
        day3 = create_day(110, 115, 109, 114)  # Open at or above the previous close
        days = pd.DataFrame([day1, day2, day3])
        assert PatternDefinitions.is_three_white_soldiers(days) == True

        day2 = create_day(103, 107, 102, 106)  # Second day opens within the body of the first day
        days = pd.DataFrame([day1, day2, day3])
        assert PatternDefinitions.is_three_white_soldiers(days) == False

    def test_is_hanging_man(self):
        prev_day = create_day(150, 155, 149, 154)  # Higher close, uptrend
        day = create_day(155, 155, 140, 148)  # Long lower shadow, bearish
        assert PatternDefinitions.is_hanging_man(day, prev_day) == True

        # day = create_day(150, 160, 149, 158)  # Does not fit the pattern
        # assert PatternDefinitions.is_hanging_man(day, prev_day) == False

    def test_is_shooting_star(self):
        prev_day = create_day(200, 205, 198, 203)  # Lower close, uptrend
        day = create_day(204, 215, 204, 205)  # Small body, long upper shadow, bearish
        assert PatternDefinitions.is_shooting_star(day, prev_day) == True

        day = create_day(204, 209, 203, 208)  # Does not fit the pattern
        assert PatternDefinitions.is_shooting_star(day, prev_day) == False

    def test_is_bearish_engulfing(self):
        prev_day = create_day(120, 125, 119, 124)
        day = create_day(125, 126, 115, 118)  # Bearish Engulfing 模式
        assert PatternDefinitions.is_bearish_engulfing(day, prev_day) == True

        day = create_day(123, 128, 122, 127)
        assert PatternDefinitions.is_bearish_engulfing(day, prev_day) == False

    def test_is_evening_star(self):
        day1 = create_day(130, 135, 129, 134)  # Bullish
        day2 = create_day(135, 136, 134, 135)  # Small body
        day3 = create_day(134, 135, 130, 131)  # Bearish and closes below the midpoint of the first day
        days = pd.DataFrame([day1, day2, day3])
        assert PatternDefinitions.is_evening_star(days) == True

        day3 = create_day(135, 138, 134, 137)  # Does not close below the midpoint
        days = pd.DataFrame([day1, day2, day3])
        assert PatternDefinitions.is_evening_star(days) == False

    def test_is_three_black_crows(self):
        day1 = create_day(120, 125, 119, 118)
        day2 = create_day(118, 123, 117, 116)
        day3 = create_day(116, 121, 115, 114)  # Three Black Crows 模式
        days = pd.DataFrame([day1, day2, day3])
        assert PatternDefinitions.is_three_black_crows(days) == True

        day2 = create_day(118, 123, 117, 120)
        days = pd.DataFrame([day1, day2, day3])
        assert PatternDefinitions.is_three_black_crows(days) == False

    def test_is_dark_cloud_cover(self):
        prev_day = create_day(150, 155, 149, 154)
        day = create_day(155, 156, 145, 148)  # Dark Cloud Cover 模式
        assert PatternDefinitions.is_dark_cloud_cover(day, prev_day) == True

        day = create_day(154, 159, 153, 158)
        assert PatternDefinitions.is_dark_cloud_cover(day, prev_day) == False


# 啟動 pytest 時，這些測試將自動運行
if __name__ == "__main__":
    pytest.main()

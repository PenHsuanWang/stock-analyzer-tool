[![Python CI](https://github.com/PenHsuanWang/stock-analyzer-tool/actions/workflows/main-ci.yml/badge.svg)](https://github.com/PenHsuanWang/stock-analyzer-tool/actions/workflows/main-ci.yml)
# Stock Analysis Toolkit

## Overview
The Stock Analysis Toolkit is a Python library designed for performing advanced financial analysis on stock market data. It includes tools for calculating various technical indicators, identifying candlestick patterns, and applying combined trading strategies.

## Features
- **Candlestick Pattern Recognition**: Identifies common candlestick patterns in stock data for insightful trend analysis.
- **Technical Indicators Calculation**: Computes key technical indicators such as Moving Averages, MACD, RSI, Bollinger Bands, and Fibonacci Retracement levels.
- **Combined Trading Strategy Application**: Integrates various indicators to form holistic trading strategies.

## Installation
To use this toolkit, clone the repository and install the required dependencies:
```bash
git clone https://github.com/your-repository/stock-analysis-toolkit.git
cd stock-analysis-toolkit
pip install -r requirements.txt
```

## Usage

### Candlestick Pattern Recognition
To recognize candlestick patterns:
```python
from src.stockana.candlestick_pattern import PatternDefinitions

# Example: Recognizing a bullish engulfing pattern
bullish_engulfing = PatternDefinitions.is_bullish_engulfing(today_data, yesterday_data)
```

### Technical Indicators Calculation
Calculate technical indicators using provided methods:
```python
from src.stockana.calc_advance_indicator import AdvancedFinancialIndicator

# Example: Calculating Exponential Moving Average (EMA)
ema = AdvancedFinancialIndicator.compute_ema(stock_data, window=20, column='Close')
```

### Combined Trading Strategy Application
Apply a combined strategy on your stock data:
```python
# Example: Applying a combined strategy
analyzed_data = AdvancedFinancialIndicator.apply_strategy(stock_data, short_window=12, long_window=26, volume_window=20)
```

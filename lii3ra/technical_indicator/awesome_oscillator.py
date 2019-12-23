
import pandas as pd


class AwesomeOscillator:
    def __init__(self, ohlcv, slow_period=34, fast_period=5):
        self.symbol = ohlcv.symbol
        self.start_date = ohlcv.start_date
        self.end_date = ohlcv.end_date
        self.ohlcv = ohlcv.values
        self.slow_period = slow_period
        self.fast_period = fast_period
        slow = pd.Series(((self.ohlcv["high"] + self.ohlcv["low"]) / 2).rolling(window=self.slow_period).mean())
        fast = pd.Series(((self.ohlcv["high"] + self.ohlcv["low"]) / 2).rolling(window=self.fast_period).mean())
        self.ao = pd.Series(fast - slow)



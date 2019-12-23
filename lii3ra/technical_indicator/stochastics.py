import pandas as pd


class Stochastic:
    """Stochastic oscillator %K
     The stochastic oscillator is a momentum indicator comparing the closing price of a security
     to the range of its prices over a certain period of time.
     The sensitivity of the oscillator to market movements is reducible by adjusting that time
     period or by taking a moving average of the result.
    """

    def __init__(self, ohlcv, period=14, smoothing1=3, smoothing2=3):
        self.symbol = ohlcv.symbol
        self.start_date = ohlcv.start_date
        self.end_date = ohlcv.end_date
        self.ohlcv = ohlcv.values
        self.period = period
        self.smoothing1 = smoothing1
        self.smoothing2 = smoothing2
        highest_high = self.ohlcv["high"].rolling(center=False, window=self.period).max()
        lowest_low = self.ohlcv["low"].rolling(center=False, window=self.period).min()
        k = pd.Series((self.ohlcv["close"] - lowest_low) / (highest_high - lowest_low))
        mult = 100
        self.fast_k = mult * k
        self.fast_d = pd.Series(self.fast_k.rolling(center=False, window=self.smoothing1).mean())
        self.slow_k = self.fast_d
        self.slow_d = pd.Series(self.slow_k.rolling(center=False, window=self.smoothing2).mean())


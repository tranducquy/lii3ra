import pandas as pd


class TriangularMovingAverage:
    def __init__(self, ohlcv, ma_span=15):
        self.symbol     = ohlcv.symbol
        self.start_date = ohlcv.start_date
        self.end_date   = ohlcv.end_date
        self.ohlcv      = ohlcv.values
        self.ma_span    = ma_span
        s = pd.Series(self.ohlcv['close'])
        self.ma = s.rolling(window=self.ma_span).mean()
        ma_sum = self.ma.rolling(window=self.ma_span).sum()
        self.trima = pd.Series(ma_sum / self.ma_span)
        s = pd.Series(self.ohlcv['low'])
        self.ma_low = s.rolling(window=self.ma_span).mean()
        ma_sum = self.ma_low.rolling(window=self.ma_span).sum()
        self.trima_low = pd.Series(ma_sum / self.ma_span)


import pandas as pd


class TriangularMovingAverage:
    def __init__(self, ohlcv, ma_span=15):
        self.symbol     = ohlcv.symbol
        self.start_date = ohlcv.start_date
        self.end_date   = ohlcv.end_date
        self.ohlcv      = ohlcv.values
        self.ma_span    = ma_span
        s = pd.Series(self.ohlcv['close'])
        self.sma = s.rolling(window=self.ma_span).mean()
        sma_sum = self.sma.rolling(window=self.ma_span).sum()
        self.trima = pd.Series(sma_sum / self.ma_span)
        s = pd.Series(self.ohlcv['low'])
        self.sma_low = s.rolling(window=self.ma_span).mean()
        sma_sum = self.sma_low.rolling(window=self.ma_span).sum()
        self.trima_low = pd.Series(sma_sum / self.ma_span)


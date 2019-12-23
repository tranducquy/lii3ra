
import pandas as pd


class SimpleMovingAverage:
    def __init__(self, ohlcv, sma_span=15, vol_sma_span=5):
        self.symbol = ohlcv.symbol
        self.start_date = ohlcv.start_date
        self.end_date = ohlcv.end_date
        self.ohlcv = ohlcv.values
        self.sma_span = sma_span
        self.vol_sma_span = vol_sma_span
        # 終値から単純移動平均を算出
        s = pd.Series(self.ohlcv['close'])
        self.sma = s.rolling(window=self.sma_span).mean()
        # 出来高から単純移動平均を算出
        s = pd.Series(self.ohlcv['volume'])
        self.vol_sma = s.rolling(window=self.vol_sma_span).mean()



import pandas as pd


class KeltnerChannels:
    def __init__(self, ohlcv, atr_span=15, kc_ratio=0.5):
        self.symbol = ohlcv.symbol
        self.start_date = ohlcv.start_date
        self.end_date = ohlcv.end_date
        self.ohlcv = ohlcv.values
        self.atr_span = atr_span
        self.kc_ratio = kc_ratio
        # 終値の指数移動平均
        s = pd.Series(self.ohlcv['close'])
        self.middle = s.ewm(span=self.atr_span).mean()
        # True Range
        self.ohlcv['tr1'] = abs(self.ohlcv['high'] - self.ohlcv['low'])
        self.ohlcv['tr2'] = abs(self.ohlcv['high'] - self.ohlcv['close'].shift())
        self.ohlcv['tr3'] = abs(self.ohlcv['low'] - self.ohlcv['close'].shift())
        self.ohlcv['tr'] = self.ohlcv[['tr1', 'tr2', 'tr3']].max(axis=1)
        # Average True RangeとしてTrue Rangeの指数移動平均
        s = pd.Series(self.ohlcv['tr'])
        self.atr = s.ewm(span=self.atr_span).mean()
        self.upper_band = pd.Series(self.middle + (self.kc_ratio * self.atr))
        self.lower_band = pd.Series(self.middle - (self.kc_ratio * self.atr))


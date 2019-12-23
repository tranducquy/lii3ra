
import pandas as pd


class AverageTrueRange:
    def __init__(self, ohlcv: object, atr_span: int = 15) -> object:
        self.symbol = ohlcv.symbol
        self.start_date = ohlcv.start_date
        self.end_date = ohlcv.end_date
        self.ohlcv = ohlcv.values
        self.atr_span = atr_span
        """終値の指数移動平均を算出する"""
        s = pd.Series(self.ohlcv['close'])
        self.ema = s.ewm(span=self.atr_span).mean()
        """True Rangeを算出する"""
        self.ohlcv['tr1'] = abs(self.ohlcv['high'] - self.ohlcv['low'])
        self.ohlcv['tr2'] = abs(self.ohlcv['high'] - self.ohlcv['close'].shift())
        self.ohlcv['tr3'] = abs(self.ohlcv['low'] - self.ohlcv['close'].shift())
        self.ohlcv['tr'] = self.ohlcv[['tr1', 'tr2', 'tr3']].max(axis=1)
        """Average True RangeとしてTrue Rangeの指数移動平均を算出する"""
        s = pd.Series(self.ohlcv['tr'])
        self.atr = s.ewm(span=self.atr_span).mean()
        """Average True Rangeとして、True Rangeの単純移動平均を算出する"""
        s = pd.Series(self.ohlcv['tr'])
        self.atr_sma = s.rolling(window=self.atr_span).mean()


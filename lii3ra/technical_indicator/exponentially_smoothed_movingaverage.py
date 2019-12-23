import pandas as pd


class ExponentiallySmoothedMovingAverage:
    def __init__(self, ohlcv, ema_span=15, vol_ema_span=5):
        self.symbol = ohlcv.symbol
        self.start_date = ohlcv.start_date
        self.end_date = ohlcv.end_date
        self.ohlcv = ohlcv.values
        self.ema_span = ema_span
        self.vol_ema_span = vol_ema_span
        # 終値から指数移動平均を算出
        s = pd.Series(self.ohlcv['close'])
        self.ema = s.ewm(span=self.ema_span).mean()
        # 出来高から指数移動平均を算出
        s = pd.Series(self.ohlcv['volume'])
        self.vol_ema = s.ewm(span=self.vol_ema_span).mean()


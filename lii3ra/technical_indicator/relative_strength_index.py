
import pandas as pd


class RelativeStrengthIndex:
    def __init__(self, ohlcv, span=14):
        self.symbol = ohlcv.symbol
        self.start_date = ohlcv.start_date
        self.end_date = ohlcv.end_date
        self.ohlcv = ohlcv.values
        self.span = span
        # 終値からRSIを算出
        close = pd.Series(self.ohlcv['close'])
        diff = close.diff()
        up = diff.copy()
        down = diff.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        self.up_ema = up.ewm(span=self.span).mean()
        self.down_ema = down.abs().ewm(span=self.span).mean()
        rs = self.up_ema / self.down_ema
        self.rsi = pd.Series(100.0 - (100.0 / (1.0 + rs)))

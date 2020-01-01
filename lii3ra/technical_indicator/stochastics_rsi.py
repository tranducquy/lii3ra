import pandas as pd


class StochasticRSI:

    def __init__(self, ohlcv, rsi_period=14, stoch_period=14):
        self.symbol = ohlcv.symbol
        self.start_date = ohlcv.start_date
        self.end_date = ohlcv.end_date
        self.ohlcv = ohlcv.values
        self.rsi_period = rsi_period
        self.stoch_period = stoch_period
        # 終値からRSIを算出
        close = pd.Series(self.ohlcv['close'])
        diff = close.diff()
        up = diff.copy()
        down = diff.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        self.up_ema = up.ewm(span=self.rsi_period).mean()
        self.down_ema = down.abs().ewm(span=self.rsi_period).mean()
        rs = self.up_ema / self.down_ema
        self.rsi = pd.Series(100.0 - (100.0 / (1.0 + rs)))
        # RSIからストキャスティクスRSIを算出
        self.stoch_rsi = pd.Series(
            ((self.rsi - self.rsi.min()) / (self.rsi.max() - self.rsi.min()))
            .rolling(window=self.stoch_period)
            .mean()
        )


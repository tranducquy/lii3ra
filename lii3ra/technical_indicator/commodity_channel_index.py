import pandas as pd


class CommodityChannelIndex:
    def __init__(self, ohlcv, period=20, constant=0.015):
        self.symbol = ohlcv.symbol
        self.start_date = ohlcv.start_date
        self.end_date = ohlcv.end_date
        self.ohlcv = ohlcv.values
        self.period = period
        self.constant = constant
        # TP(Typical Price)からCCIを算出 Typical Price=(高値+安値+終値)/3
        self.tp = pd.Series((self.ohlcv["high"] + self.ohlcv["low"] + self.ohlcv["close"]) / 3)
        tp_rolling = self.tp.rolling(window=self.period, min_periods=0)
        self.cci = pd.Series((self.tp - tp_rolling.mean()) / (self.constant * tp_rolling.std()))

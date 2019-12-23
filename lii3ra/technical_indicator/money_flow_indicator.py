
import pandas as pd


class MoneyFlowIndicator:
    def __init__(self, ohlcv, period=20):
        self.symbol = ohlcv.symbol
        self.start_date = ohlcv.start_date
        self.end_date = ohlcv.end_date
        self.ohlcv = ohlcv.values
        self.period = period
        self.tp = None
        self.rmf = None
        self.mfi = None
        self.set_mfi()

    def set_mfi(self):
        self.tp = pd.Series((self.ohlcv["high"] + self.ohlcv["low"] + self.ohlcv["close"]) / 3, name="TP")
        self.rmf = pd.Series(self.tp * self.ohlcv["volume"], name="rmf")  ## Real Money Flow
        _mf = pd.concat([self.tp, self.rmf], axis=1)
        _mf["delta"] = _mf["TP"].diff()

        def pos(row):
            if row["delta"] > 0:
                return row["rmf"]
            else:
                return 0

        def neg(row):
            if row["delta"] < 0:
                return row["rmf"]
            else:
                return 0

        _mf["neg"] = _mf.apply(neg, axis=1)
        _mf["pos"] = _mf.apply(pos, axis=1)
        mfratio = pd.Series(_mf["pos"].rolling(window=self.period).sum() / _mf["neg"].rolling(window=self.period).sum())
        self.mfi = pd.Series(100 - (100 / (1 + mfratio)))


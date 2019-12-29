import pandas as pd


class UltimateOscillator:
    """Ultimate Oscillator is a momentum oscillator designed to capture momentum across three different time frames.
    The multiple time frame objective seeks to avoid the pitfalls of other oscillators.
    Many momentum oscillators surge at the beginning of a strong advance and then form bearish divergence as the advance continues.
    This is because they are stuck with one time frame. The Ultimate Oscillator attempts to correct this fault by incorporating longer
    time frames into the basic formula."""

    def __init__(self, ohlcv, avg1=7, avg2=14, avg3=28):
        self.symbol = ohlcv.symbol
        self.start_date = ohlcv.start_date
        self.end_date = ohlcv.end_date
        self.ohlcv = ohlcv.values
        self.avg1 = avg1
        self.avg2 = avg2
        self.avg3 = avg3
        # True Rangeを算出する
        self.ohlcv['tr1'] = abs(self.ohlcv['high'] - self.ohlcv['low'])
        self.ohlcv['tr2'] = abs(self.ohlcv['high'] - self.ohlcv['close'].shift())
        self.ohlcv['tr3'] = abs(self.ohlcv['low'] - self.ohlcv['close'].shift())
        self.tr = self.ohlcv[['tr1', 'tr2', 'tr3']].max(axis=1)
        k = []  # current low or past close
        df = pd.DataFrame(self.ohlcv)
        for row, _row in zip(df.itertuples(), df.shift(1).itertuples()):
            k.append(min(row.low, _row.close))
        bp = pd.Series(self.ohlcv["close"] - k)
        average1 = bp.rolling(window=self.avg1).sum() / self.tr.rolling(window=self.avg1).sum()
        average2 = bp.rolling(window=self.avg2).sum() / self.tr.rolling(window=self.avg2).sum()
        average3 = bp.rolling(window=self.avg3).sum() / self.tr.rolling(window=self.avg3).sum()
        self.uo = pd.Series((100 * ((4 * average1) + (2 * average2) + average3)) / (4 + 2 + 1))


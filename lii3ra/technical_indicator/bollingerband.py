
import pandas as pd


class Bollingerband:
    def __init__(self, ohlcv, sma_span, sigma1_ratio=1.0, sigma2_ratio=2.0, sigma3_ratio=3.0):
        self.symbol = ohlcv.symbol
        self.start_date = ohlcv.start_date
        self.end_date = ohlcv.end_date
        self.ohlcv = ohlcv.values
        self.sma_span = sma_span
        self.sigma1_ratio = sigma1_ratio
        self.sigma2_ratio = sigma2_ratio
        self.sigma3_ratio = sigma3_ratio
        # 終値からボリンジャーバンドを生成
        s = pd.Series(self.ohlcv['close'])
        self.sma = s.rolling(window=self.sma_span).mean()
        self.sigma = s.rolling(window=self.sma_span).std(ddof=0)
        self.upper_sigma1 = self.sma + self.sigma * self.sigma1_ratio
        self.lower_sigma1 = self.sma - self.sigma * self.sigma1_ratio
        self.upper_sigma2 = self.sma + self.sigma * self.sigma2_ratio
        self.lower_sigma2 = self.sma - self.sigma * self.sigma2_ratio
        self.upper_sigma3 = self.sma + self.sigma * self.sigma3_ratio
        self.lower_sigma3 = self.sma - self.sigma * self.sigma3_ratio


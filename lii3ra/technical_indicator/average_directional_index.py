

class AverageDirectionalIndex:
    def __init__(self, ohlcv, adx_span=14, adxr_span=28):
        self.symbol = ohlcv.symbol
        self.start_date = ohlcv.start_date
        self.end_date = ohlcv.end_date
        self.ohlcv = ohlcv.values
        self.adx_span = adx_span
        self.adxr_span = adxr_span
        # dm
        pdm = self.ohlcv['high'] - self.ohlcv['high'].shift()
        mdm = self.ohlcv['low'].shift() - self.ohlcv['low']
        pdm[pdm[:] < 0] = 0
        mdm[mdm[:] < 0] = 0
        mdm[pdm[:] > mdm[:]] = 0
        pdm[mdm[:] > pdm[:]] = 0
        # tr
        self.ohlcv['tr1'] = abs(self.ohlcv['high'] - self.ohlcv['low'])
        self.ohlcv['tr2'] = abs(self.ohlcv['high'] - self.ohlcv['close'].shift())
        self.ohlcv['tr3'] = abs(self.ohlcv['low'] - self.ohlcv['close'].shift())
        self.tr = self.ohlcv[['tr1', 'tr2', 'tr3']].max(axis=1)
        # di
        self.pdi = pdm.rolling(window=self.adx_span).sum() / self.tr.rolling(window=self.adx_span).sum()  # +DI
        self.mdi = mdm.rolling(window=self.adx_span).sum() / self.tr.rolling(window=self.adx_span).sum()  # -DI
        # adx
        self.dx = (self.pdi - self.mdi).abs() / (self.pdi + self.mdi)
        self.adx = self.dx.ewm(span=self.adx_span).mean()
        # adxr
        self.adxr = self.adx.ewm(span=self.adxr_span).mean()

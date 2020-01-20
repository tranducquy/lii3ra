import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.simple_movingaverage import SimpleMovingAverage
from lii3ra.technical_indicator.exponentially_smoothed_movingaverage import ExponentiallySmoothedMovingAverage
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class MAWithTwistFactory(EntryStrategyFactory):
    params = {
        # fast_ma_span, slow_ma_span
        "default": [1, 10, 20, 0.005]
        # , "^N225": [3, 1.0, 3, 1.0]
    }

    def create(self, ohlcv, optimization=False):
        strategies = []
        if not optimization:
            #
            s = ohlcv.symbol
            if s in self.params:
                imethod = self.params[s][0]
                fast_ma_span = self.params[s][1]
                slow_ma_span = self.params[s][2]
                threshold = self.params[s][3]
            else:
                imethod = self.params["default"][0]
                fast_ma_span = self.params["default"][1]
                slow_ma_span = self.params["default"][2]
                threshold = self.params["default"][3]
            strategies.append(MAWithTwist(ohlcv, imethod, fast_ma_span, slow_ma_span, threshold))
        else:
            imethods = [1, 2]
            fast_spans = [i for i in range(3, 10, 2)]
            slow_spans = [i for i in range(10, 30, 4)]
            thresholds = [i for i in np.arange(0.10, 0.80, 0.10)]
            for fast_span in fast_spans:
                for slow_span in slow_spans:
                    for imethod in imethods:
                        for threshold in thresholds:
                            strategies.append(MAWithTwist(ohlcv, imethod, fast_span, slow_span, threshold))
        return strategies


class MAWithTwist(EntryStrategy):
    """
    移動平均の短期と長期を用いて移動平均のクロスと、指定の閾値を比較し、次のバーで成行エントリーする
    """

    def __init__(self
                 , ohlcv
                 , imethod
                 , fast_ma_span
                 , slow_ma_span
                 , price_threshold
                 , order_vol_ratio=0.01):
        self.title = f"MAWithTwist[{imethod:.0f}][{fast_ma_span:.0f},{slow_ma_span:.0f},{price_threshold:.2f}]"
        self.ohlcv = ohlcv
        self.fast_ma = None
        self.slow_ma = None
        self.imethod = imethod
        if imethod == 1:
            self.fast_ma = SimpleMovingAverage(ohlcv, fast_ma_span)
            self.slow_ma = SimpleMovingAverage(ohlcv, slow_ma_span)
        else:
            self.fast_ma = ExponentiallySmoothedMovingAverage(ohlcv, fast_ma_span)
            self.slow_ma = ExponentiallySmoothedMovingAverage(ohlcv, slow_ma_span)
        self.price_threshold = price_threshold
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if self.imethod == 1:
            if self.fast_ma.sma[idx] == 0 or self.slow_ma.sma[idx] == 0:
                return False
        else:
            if self.fast_ma.ema[idx] == 0 or self.slow_ma.ema[idx] == 0:
                return False
        return True

    def check_entry_long(self, idx, last_exit_idx):
        """
        短期MAが長期MAを下から上に抜けてクロスした直後に現在の終値が閾値より下にある場合、次のバーで新規成行買
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx == 0:
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        low = self.ohlcv.values['low'][idx]
        if self.imethod == 1:
            fast_ma_before = self.fast_ma.sma[idx - 1]
            fast_ma_current = self.fast_ma.sma[idx]
            slow_ma_before = self.slow_ma.sma[idx - 1]
            slow_ma_current = self.slow_ma.sma[idx]
        else:
            fast_ma_before = self.fast_ma.ema[idx - 1]
            fast_ma_current = self.fast_ma.ema[idx]
            slow_ma_before = self.slow_ma.ema[idx - 1]
            slow_ma_current = self.slow_ma.ema[idx]
        above_cross_flg = fast_ma_before < slow_ma_before and fast_ma_current > slow_ma_current
        threshold_flg = close < low + (close * self.price_threshold)
        if above_cross_flg and threshold_flg:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        短期MAが長期MAを上から下に抜けてクロスした直後に現在の終値が閾値より上にある場合、次のバーで新規成行売
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx == 0:
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        high = self.ohlcv.values['high'][idx]
        if self.imethod == 1:
            fast_ma_before = self.fast_ma.sma[idx - 1]
            fast_ma_current = self.fast_ma.sma[idx]
            slow_ma_before = self.slow_ma.sma[idx - 1]
            slow_ma_current = self.slow_ma.sma[idx]
        else:
            fast_ma_before = self.fast_ma.ema[idx - 1]
            fast_ma_current = self.fast_ma.ema[idx]
            slow_ma_before = self.slow_ma.ema[idx - 1]
            slow_ma_current = self.slow_ma.ema[idx]
        below_cross_flg = fast_ma_before > slow_ma_before and fast_ma_current < slow_ma_current
        threshold_flg = close > high - (close * self.price_threshold)
        if below_cross_flg and threshold_flg:
            return OrderType.MARKET_SHORT
        else:
            return OrderType.NONE_ORDER

    def create_order_entry_long_stop_market_for_all_cash(self, cash, idx, last_exit_idx):
        if not self._is_valid(idx) or cash <= 0:
            return -1, -1
        price = self.create_order_entry_long_stop_market(idx, last_exit_idx)
        vol = self.get_order_vol(cash, idx, price, last_exit_idx)
        return price, vol

    def create_order_entry_short_stop_market_for_all_cash(self, cash, idx, last_exit_idx):
        if not self._is_valid(idx) or cash <= 0:
            return -1, -1
        price = self.create_order_entry_short_stop_market(idx, last_exit_idx)
        vol = self.get_order_vol(cash, idx, price, last_exit_idx)
        return price, vol * -1

    def create_order_entry_long_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        return 0.00

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        return 0.00

    def create_order_entry_long_market_for_all_cash(self, cash, idx, last_exit_idx):
        if not self._is_valid(idx) or cash <= 0:
            return -1, -1
        price = self.ohlcv.values['close'][idx]
        vol = self.get_order_vol(cash, idx, price, last_exit_idx)
        return price, vol

    def create_order_entry_short_market_for_all_cash(self, cash, idx, last_exit_idx):
        if not self._is_valid(idx) or cash <= 0:
            return -1, -1
        price = self.ohlcv.values['close'][idx]
        vol = self.get_order_vol(cash, idx, price, last_exit_idx)
        return price, vol * -1

    def get_indicators(self, idx, last_exit_idx):
        ind1 = self.fast_ma.sma[idx] if self.imethod == 1 else self.fast_ma.ema[idx]
        ind2 = self.slow_ma.sma[idx] if self.imethod == 1 else self.slow_ma.ema[idx]
        ind3 = None
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

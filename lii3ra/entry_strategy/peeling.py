import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.simple_movingaverage import SimpleMovingAverage
from lii3ra.technical_indicator.exponentially_smoothed_movingaverage import ExponentiallySmoothedMovingAverage
from lii3ra.technical_indicator.triangular_movingaverage import TriangularMovingAverage
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class PeelingFactory(EntryStrategyFactory):
    params = {
        # imethod, ma_span, long_peeling_ratio, short_peeling_ratio
        "default": [1, 15, -0.15, 0.15]
        , "^N225": [2, 10, -0.15, 0.15]
    }

    rough_params = [
        [1, 25, 1.0, -1.0]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            imethod = self.params[s][0]
            span = self.params[s][1]
            long_peeling_ratio = self.params[s][2]
            short_peeling_ratio = self.params[s][3]
        else:
            imethod = self.params["default"][0]
            span = self.params["default"][1]
            long_peeling_ratio = self.params["default"][2]
            short_peeling_ratio = self.params["default"][3]
        return Peeling(ohlcv, imethod, span, long_peeling_ratio, short_peeling_ratio)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            #
            for p in self.rough_params:
                strategies.append(Peeling(ohlcv
                                          , p[0]
                                          , p[1]
                                          , p[2]
                                          , p[3]))
        else:
            imethods = [1, 2, 3]
            span_list = [i for i in range(5, 31, 5)]
            long_peeling_ratio_list = [i*-1 for i in np.arange(0.2, 1.2, 0.3)]
            short_peeling_ratio_list = [i for i in np.arange(0.2, 1.2, 0.3)]
            for imethod in imethods:
                for span in span_list:
                    for long_peeling_ratio in long_peeling_ratio_list:
                        for short_peeling_ratio in short_peeling_ratio_list:
                            strategies.append(Peeling(ohlcv, imethod, span, long_peeling_ratio, short_peeling_ratio))
        return strategies


class Peeling(EntryStrategy):
    """
    移動平均乖離率でやっちゃう
    """

    def __init__(self
                 , ohlcv
                 , imethod
                 , span
                 , long_peeling_ratio
                 , short_peeling_ratio
                 , order_vol_ratio=0.01):
        self.title = f"Peeling[{imethod:.0f}][{span:.0f}][{long_peeling_ratio:.2f},{short_peeling_ratio:.2f}]"
        self.ohlcv = ohlcv
        self.ma = None
        self.imethod = imethod
        if imethod == 1:
            self.ma = SimpleMovingAverage(ohlcv, span)
        elif imethod == 2:
            self.ma = ExponentiallySmoothedMovingAverage(ohlcv, span)
        else:
            self.ma = TriangularMovingAverage(ohlcv, span)
        self.long_peeling_ratio = long_peeling_ratio
        self.short_peeling_ratio = short_peeling_ratio
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio
        self.ma_value = 0
        self.peeling_value = 0

    def _is_indicator_valid(self, idx):
        if self.imethod == 1:
            if self.ma.sma[idx] == 0:
                return False
        elif self.imethod == 2:
            if self.ma.ema[idx] == 0:
                return False
        else:
            if self.ma.trima_low[idx] == 0:
                return False
        return True

    def check_entry_long(self, idx, last_exit_idx):
        """
        移動平均乖離率が指定した値よりも小さければロング
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx == 0:
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        if self.imethod == 1:
            self.ma_value = self.ma.sma[idx]
        elif self.imethod == 2:
            self.ma_value = self.ma.ema[idx]
        else:
            self.ma_value = self.ma.trima_low[idx]
        self.peeling_value = (close - self.ma_value) / self.ma_value
        long_condition = self.long_peeling_ratio > self.peeling_value
        if long_condition:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        移動平均乖離率が指定した値よりも大きければショート
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx == 0:
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        if self.imethod == 1:
            self.ma_value = self.ma.sma[idx - 1]
        elif self.imethod == 2:
            self.ma_value = self.ma.ema[idx - 1]
        else:
            self.ma_value = self.ma.trima_low[idx - 1]
        self.peeling_value = (close - self.ma_value) / self.ma_value
        short_condition = self.short_peeling_ratio < self.peeling_value
        if short_condition:
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
        ind1 = self.ma_value
        ind2 = self.long_peeling_ratio
        ind3 = self.short_peeling_ratio
        ind4 = self.peeling_value
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

import math
import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.average_true_range import AverageTrueRange
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class ATRBasedBreakoutOneSideFactory(EntryStrategyFactory):
    params = {
        # long_atr_span, long_atr_ratio, short_atr_span, short_atr_ratio
        "default": [15, 1.0, 3, 100.0]
        # , "4043.T": [13, 0.3, 3, 0.3]
        # , "3064.T": [18, 0.3, 28, 0.3]
        # , "2267.T": [18, 0.3, 3, 0.3]
    }

    def create(self, ohlcv, optimization=False):
        strategies = []
        if not optimization:
            #
            s = ohlcv.symbol
            if s in self.params:
                long_span = self.params[s][0]
                long_ratio = self.params[s][1]
                short_span = self.params[s][2]
                short_ratio = self.params[s][3]
            else:
                long_span = self.params["default"][0]
                long_ratio = self.params["default"][1]
                short_span = self.params["default"][2]
                short_ratio = self.params["default"][3]
            strategies.append(ATRBasedBreakoutOneSide(ohlcv, long_span, long_ratio, short_span, short_ratio))
        else:
            long_spans = [i for i in range(2, 30, 3)]
            long_ratios = [i for i in np.arange(0.1, 1.6, 0.2)]
            short_spans = [i for i in range(2, 30, 3)]
            short_ratios = [i for i in np.arange(0.1, 1.6, 0.2)]
            for long_span in long_spans:
                for long_ratio in long_ratios:
                    strategies.append(ATRBasedBreakoutOneSide(ohlcv, long_span, long_ratio, 3, 0.0))
            for short_span in short_spans:
                for short_ratio in short_ratios:
                    strategies.append(ATRBasedBreakoutOneSide(ohlcv, 3, 0.0, short_span, short_ratio))
        return strategies


class ATRBasedBreakoutOneSide(EntryStrategy):
    """
    Long:終値+(ATR*XX)に逆指値注文する
    Short:終値-(ATR*XX)に逆指値注文する
    """

    def __init__(self, ohlcv, long_atr_span, long_atr_ratio, short_atr_span, short_atr_ratio,
                 order_vol_ratio=0.01):
        self.title = f"ATRBasedBreakoutOneSide[{long_atr_span:.0f},{long_atr_ratio:.1f}]" \
                     f"[{short_atr_span:.0f},{short_atr_ratio:.1f}]"
        self.ohlcv = ohlcv
        self.long_atr = AverageTrueRange(ohlcv, long_atr_span)
        self.long_atr_ratio = long_atr_ratio
        self.short_atr = AverageTrueRange(ohlcv, short_atr_span)
        self.short_atr_ratio = short_atr_ratio
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.long_atr.atr[idx] == 0
                or self.short_atr.atr[idx] == 0):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.long_atr.atr_span:
            return OrderType.NONE_ORDER
        if self.long_atr_ratio == 0:
            return OrderType.NONE_ORDER
        else:
            return OrderType.STOP_MARKET_LONG

    def check_entry_short(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.short_atr.atr_span:
            return OrderType.NONE_ORDER
        if self.short_atr_ratio == 0:
            return OrderType.NONE_ORDER
        else:
            return OrderType.STOP_MARKET_SHORT

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
        close = self.ohlcv.values['close'][idx]
        atrband = math.ceil(self.long_atr.atr[idx] * self.long_atr_ratio)
        price = close + atrband
        return price

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        close = self.ohlcv.values['close'][idx]
        atrband = math.floor(self.short_atr.atr[idx] * self.short_atr_ratio)
        price = close - atrband
        return price

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
        ind1 = self.long_atr.ema[idx]
        ind2 = self.long_atr.atr[idx]
        ind3 = self.long_atr.atr[idx] * self.long_atr_ratio
        ind4 = self.short_atr.ema[idx]
        ind5 = self.short_atr.atr[idx]
        ind6 = self.short_atr.atr[idx] * self.short_atr_ratio
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

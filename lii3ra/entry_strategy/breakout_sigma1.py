import math
import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.tick import Tick
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy
from lii3ra.technical_indicator.bollingerband import Bollingerband


class BreakoutSigma1Factory(EntryStrategyFactory):
    params = {
        # long_bb_span, long_bb_ratio, short_bb_span, short_bb_ratio
        "default": [3, 1.0, 3, 1.0, 1]
        , "^N225": [10, 0.9, 3, 1.4, 1]
        , "DJI": [8, 0.6, 13, 0.6, 1]
        , "TREIT": [8, 0.6, 18, 1.2, 1]
        , "1568.T": [3, 1.2, 18, 1.2, 1]
        , "1570.T": [3, 1.2, 3, 1.8, 1]
        , "5706.T": [23, 0.5, 21, 0.2, 1]
        , "6141.T": [3, 1.2, 8, 0.6, 2]  # 2020.01.19-
        , "6166.T": [3, 0.9, 8, 0.3, 2]
        , "6753.T": [8, 0.5, 7, 1.1, 1]
        , "9104.T": [13, 0.6, 8, 0.9, 1]
        , "9107.T": [13, 0.9, 13, 0.9, 1]
    }

    def create(self, ohlcv, optimization=False):
        strategies = []
        if not optimization:
            #
            s = ohlcv.symbol
            if s in self.params:
                long_bb_span = self.params[s][0]
                long_bb_ratio = self.params[s][1]
                short_bb_span = self.params[s][2]
                short_bb_ratio = self.params[s][3]
                stop_order = self.params[s][4]
            else:
                long_bb_span = self.params["default"][0]
                long_bb_ratio = self.params["default"][1]
                short_bb_span = self.params["default"][2]
                short_bb_ratio = self.params["default"][3]
                stop_order = self.params["default"][4]
            strategies.append(BreakoutSigma1(ohlcv
                                             , long_bb_span
                                             , long_bb_ratio
                                             , short_bb_span
                                             , short_bb_ratio
                                             , stop_order))
        else:
            long_spans = [i for i in range(3, 25, 5)]
            long_ratios = [i for i in np.arange(0.3, 1.5, 0.3)]
            # long_ratios = [i for i in np.arange(0.05, 1.0, 0.15)]
            short_spans = [i for i in range(3, 25, 5)]
            short_ratios = [i for i in np.arange(0.3, 1.5, 0.3)]
            # short_ratios = [i for i in np.arange(0.05, 1.0, 0.15)]
            stop_order_list = [1, 2]
            for long_span in long_spans:
                for long_ratio in long_ratios:
                    for stop_order in stop_order_list:
                        strategies.append(BreakoutSigma1(ohlcv, long_span, long_ratio, 1, 0.0, stop_order))
            for short_span in short_spans:
                for short_ratio in short_ratios:
                    for stop_order in stop_order_list:
                        strategies.append(BreakoutSigma1(ohlcv, 1, 0.0, short_span, short_ratio, stop_order))
            for long_span in long_spans:
                for long_ratio in long_ratios:
                    for short_span in short_spans:
                        for short_ratio in short_ratios:
                            for stop_order in stop_order_list:
                                strategies.append(BreakoutSigma1(ohlcv, long_span, long_ratio
                                                                 , short_span, short_ratio, stop_order))
        return strategies


class BreakoutSigma1(EntryStrategy):
    """
    高値または安値がボリンジャーバンドのシグマ1を超えた場合に逆指値注文する
    """

    def __init__(self
                 , ohlcv
                 , long_bb_span
                 , long_bb_ratio
                 , short_bb_span
                 , short_bb_ratio
                 , stop_order=1
                 , order_vol_ratio=0.01):
        self.title = f"BreakOutSigma1[{stop_order:.0f}][{long_bb_span:.0f},{long_bb_ratio:.2f}][{short_bb_span:.0f},{short_bb_ratio:.2f}]"
        self.ohlcv = ohlcv
        self.long_bb = Bollingerband(ohlcv, long_bb_span, long_bb_ratio)
        self.short_bb = Bollingerband(ohlcv, short_bb_span, short_bb_ratio)
        self.stop_order = stop_order
        self.symbol = self.ohlcv.symbol
        self.tick = Tick.get_tick(self.symbol)
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.long_bb.upper_sigma1[idx] == 0
                or self.long_bb.lower_sigma1[idx] == 0
                or self.long_bb.sma[idx] == 0
                or self.short_bb.upper_sigma1[idx] == 0
                or self.short_bb.lower_sigma1[idx] == 0
                or self.short_bb.sma[idx] == 0):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        # 当日高値がsigma1以上
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.long_bb.span:
            return OrderType.NONE_ORDER
        if self.long_bb.sigma1_ratio == 0:
            return OrderType.NONE_ORDER
        long_flg = self.ohlcv.values['high'][idx] >= self.long_bb.upper_sigma1[idx]
        short_flg = self.ohlcv.values['low'][idx] <= self.long_bb.lower_sigma1[idx]
        if long_flg and not short_flg:
            return OrderType.STOP_MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        # 当日安値がsigma1以下
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.short_bb.span:
            return OrderType.NONE_ORDER
        if self.short_bb.sigma1_ratio == 0:
            return OrderType.NONE_ORDER
        long_flg = self.ohlcv.values['high'][idx] >= self.short_bb.upper_sigma1[idx]
        short_flg = self.ohlcv.values['low'][idx] <= self.short_bb.lower_sigma1[idx]
        if not long_flg and short_flg:
            return OrderType.STOP_MARKET_SHORT
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
        if self.stop_order == 1:
            price = self.ohlcv.values['high'][idx] + self.tick
        else:
            price = self.long_bb.upper_sigma1[idx]
        return math.ceil(price)

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        if self.stop_order == 1:
            price = self.ohlcv.values['low'][idx] - self.tick
        else:
            price = self.short_bb.lower_sigma1[idx]
        return math.floor(price)

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
        ind1 = self.long_bb.sma[idx]
        ind2 = self.long_bb.upper_sigma1[idx]
        ind3 = self.long_bb.lower_sigma1[idx]
        ind4 = self.short_bb.sma[idx]
        ind5 = self.short_bb.upper_sigma1[idx]
        ind6 = self.short_bb.lower_sigma1[idx]
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

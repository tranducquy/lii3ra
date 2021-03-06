import math
import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.keltner_channels import KeltnerChannels
from lii3ra.tick import Tick
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class BreakoutKCFactory(EntryStrategyFactory):
    params = {
        # long_atr_span, long_kc_ratio, short_atr_span, short_kc_ratio
        # "default": [15, 0.5, 15, 0.5, 1, False]
        "default": [8, 0.3, 8, 0.3, 2, True]
        , "^N225": [3, 0.3, 3, 0.5, 2, False]
        , "DJI": [8, 0.5, 8, 0.5, 1, True]
        , "Topix": [3, 0.3, 3, 0.5, 2, False]
        , "Mothers": [3, 0.4, 3, 0.4, 2, True]
        , "1419.T": [13, 0.6, 3, 0.4, 1, True]
        # , "3990.T": [3, 1.0, 13, 1.0, 2, True]
        , "4043.T": [15, 0.5, 15, 0.5, 1, False]
        , "5706.T": [15, 0.5, 15, 0.5, 1, False]
        , "6479.T": [15, 0.5, 15, 0.5, 1, False]
        , "6753.T": [8, 0.6, 8, 0.3, 1, False]
        , "6920.T": [13, 0.6, 3, 1.5, 1, False]  # 2020.01.06
        , "7717.T": [18, 1.2, 8, 0.6, 1, False]
        , "9616.T": [3, 0.3, 23, 0.3, 1, False]
    }

    def create_anyspan(self, ohlcv, span, optimization=False):
        long_span = span
        long_ratio = self.params["default"][1]
        short_span = span
        short_ratio = self.params["default"][3]
        stop_order = self.params["default"][4]
        severe = self.params["default"][5]
        strategies = [BreakoutKC(ohlcv, long_span, long_ratio, short_span, short_ratio, stop_order, severe)]
        return strategies

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
                stop_order = self.params[s][4]
                severe = self.params[s][5]
            else:
                long_span = self.params["default"][0]
                long_ratio = self.params["default"][1]
                short_span = self.params["default"][2]
                short_ratio = self.params["default"][3]
                stop_order = self.params["default"][4]
                severe = self.params["default"][5]
            strategies.append(BreakoutKC(ohlcv, long_span, long_ratio, short_span, short_ratio, stop_order, severe))
        else:
            long_span_list = [i for i in range(3, 15, 5)]
            # long_ratio_list = [i for i in np.arange(0.3, 1.6, 0.2)]
            long_ratio_list = [0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]
            # long_ratio_list = [i for i in np.arange(0.01, 0.3, 0.03)]
            short_span_list = [i for i in range(3, 15, 5)]
            # short_ratio_list = [i for i in np.arange(0.3, 1.6, 0.2)]
            short_ratio_list = [0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]
            # short_ratio_list = [i for i in np.arange(0.01, 0.3, 0.03)]
            stop_order_list = [1, 2]
            # stop_order_list = [2]
            severe = True
            for long_span in long_span_list:
                for long_ratio in long_ratio_list:
                    for stop_order in stop_order_list:
                        strategies.append(BreakoutKC(ohlcv, long_span, long_ratio, 3, 100.0, stop_order, severe))
            for short_span in short_span_list:
                for short_ratio in short_ratio_list:
                    for stop_order in stop_order_list:
                        strategies.append(BreakoutKC(ohlcv, 3, 100.0, short_span, short_ratio, stop_order, severe))
            for long_span in long_span_list:
                for long_ratio in long_ratio_list:
                    for short_span in short_span_list:
                        for short_ratio in short_ratio_list:
                            for stop_order in stop_order_list:
                                strategies.append(BreakoutKC(ohlcv, long_span, long_ratio
                                                             , short_span, short_ratio, stop_order, severe))
        return strategies


class BreakoutKC(EntryStrategy):
    """
    高値または安値がバンドを超えた場合に逆指値注文する
    """

    def __init__(self
                 , ohlcv
                 , long_atr_span
                 , long_kc_ratio
                 , short_atr_span
                 , short_kc_ratio
                 , stop_order=1
                 , severe=False
                 , order_vol_ratio=0.01):
        severe_title = 1 if severe else 0
        self.title = f"BreakoutKC[{stop_order:.0f}][{long_atr_span:.0f},{long_kc_ratio:.2f}][{short_atr_span:.0f},{short_kc_ratio:.2f}][{severe_title:.0f}]"
        self.ohlcv = ohlcv
        self.long_kc = KeltnerChannels(ohlcv, long_atr_span, long_kc_ratio)
        self.short_kc = KeltnerChannels(ohlcv, short_atr_span, short_kc_ratio)
        self.stop_order = stop_order
        self.severe = severe
        self.symbol = self.ohlcv.symbol
        self.tick = Tick.get_tick(self.symbol)
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.long_kc.upper_band[idx] == 0
                or self.long_kc.lower_band[idx] == 0
                or self.short_kc.upper_band[idx] == 0
                or self.short_kc.lower_band[idx] == 0):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        # 当日高値がバンド以上
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.long_kc.atr_span:
            return OrderType.NONE_ORDER
        upper_band = self.long_kc.upper_band[idx]
        lower_band = self.long_kc.lower_band[idx]
        high = self.ohlcv.values['high'][idx]
        low = self.ohlcv.values['low'][idx]
        long_flg = high >= upper_band
        short_flg = low <= lower_band
        if self.severe and long_flg and not short_flg:
            return OrderType.STOP_MARKET_LONG
        if not self.severe and long_flg:
            return OrderType.STOP_MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        # 当日安値がバンド以下
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.short_kc.atr_span:
            return OrderType.NONE_ORDER
        upper_band = self.short_kc.upper_band[idx]
        lower_band = self.short_kc.lower_band[idx]
        high = self.ohlcv.values['high'][idx]
        low = self.ohlcv.values['low'][idx]
        long_flg = high >= upper_band
        short_flg = low <= lower_band
        if self.severe and not long_flg and short_flg:
            return OrderType.STOP_MARKET_SHORT
        if not self.severe and short_flg:
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
            price = self.long_kc.upper_band[idx]
        return math.ceil(price)

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        if self.stop_order == 1:
            price = self.ohlcv.values['low'][idx] - self.tick
        else:
            price = self.short_kc.lower_band[idx]
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
        ind1 = self.long_kc.upper_band[idx]
        ind2 = self.long_kc.lower_band[idx]
        ind3 = self.short_kc.upper_band[idx]
        ind4 = self.short_kc.lower_band[idx]
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

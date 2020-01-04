import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.keltner_channels import KeltnerChannels
from lii3ra.tick import Tick
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class BreakoutKCFactory(EntryStrategyFactory):
    params = {
        # long_atr_span, long_kc_ratio, short_atr_span, short_kc_ratio
        "default": [15, 0.5, 15, 0.5]
        , "^N225": [3, 0.3, 8, 0.3]
    }

    rough_params = [
        [10, 0.3, 10, 0.3]
        , [15, 0.3, 15, 0.3]
        , [20, 0.3, 20, 0.3]
        , [10, 0.5, 10, 0.5]
        , [15, 0.5, 15, 0.5]
        , [20, 0.5, 20, 0.5]
        , [10, 0.7, 10, 0.7]
        , [15, 0.7, 15, 0.7]
        , [20, 0.7, 20, 0.7]
    ]

    def create_strategy(self, ohlcv):
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
        return BreakoutKC(ohlcv, long_span, long_ratio, short_span, short_ratio)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            for p in self.rough_params:
                strategies.append(BreakoutKC(ohlcv
                                             , p[0]
                                             , p[1]
                                             , p[2]
                                             , p[3]))
        else:
            long_spans = [i for i in range(3, 25, 5)]
            long_ratios = [i for i in np.arange(0.3, 1.6, 0.3)]
            short_spans = [i for i in range(3, 25, 5)]
            short_ratios = [i for i in np.arange(0.3, 1.6, 0.3)]
            for long_span in long_spans:
                for long_ratio in long_ratios:
                    strategies.append(BreakoutKC(ohlcv, long_span, long_ratio, 3, 100))
            for short_span in short_spans:
                for short_ratio in short_ratios:
                    strategies.append(BreakoutKC(ohlcv, 3, 100, short_span, short_ratio))
        return strategies


class BreakoutKC(EntryStrategy):
    """高値または安値がバンドを超えた場合に逆指値注文する"""

    def __init__(self
                 , ohlcv
                 , long_atr_span
                 , long_kc_ratio
                 , short_atr_span
                 , short_kc_ratio
                 , order_vol_ratio=0.01):
        self.title = f"BreakoutKC[{long_atr_span:.0f},{long_kc_ratio:.1f}][{short_atr_span:.0f},{short_kc_ratio:.1f}]"
        self.ohlcv = ohlcv
        self.long_kc = KeltnerChannels(ohlcv, long_atr_span, long_kc_ratio)
        self.short_kc = KeltnerChannels(ohlcv, short_atr_span, short_kc_ratio)
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
        if long_flg and short_flg is not True:
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
        if long_flg is not True and short_flg:
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
        price = self.ohlcv.values['high'][idx] + self.tick
        # price = self.ohlcv.values['close'][idx] + self.long_kc.atr[idx] + self.tick
        return price

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        price = self.ohlcv.values['low'][idx] - self.tick
        # price = self.ohlcv.values['close'][idx] + self.short_kc.atr[idx] - self.tick
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
        ind1 = self.long_kc.upper_band[idx]
        ind2 = self.long_kc.lower_band[idx]
        ind3 = self.short_kc.upper_band[idx]
        ind4 = self.short_kc.lower_band[idx]
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.commodity_channel_index import CommodityChannelIndex
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class EntryCommodityChannelIndexFactory(EntryStrategyFactory):
    params = {
        # cci_period, cci_constant, cci_avg_length, long_cci_ratio, short_cci_ratio
        "default": [14, 0.015, 9, -100, 100]
    }

    def create(self, ohlcv, optimization=False):
        strategies = []
        if not optimization:
            #
            s = ohlcv.symbol
            if s in self.params:
                cci_period = self.params[s][0]
                cci_constant = self.params[s][1]
                cci_avg_length = self.params[s][2]
                long_cci_ratio = self.params[s][3]
                short_cci_ratio = self.params[s][4]
            else:
                cci_period = self.params["default"][0]
                cci_constant = self.params["default"][1]
                cci_avg_length = self.params["default"][2]
                long_cci_ratio = self.params["default"][3]
                short_cci_ratio = self.params["default"][4]
            strategies.append(EntryCommodityChannelIndex(ohlcv
                                              , cci_period, cci_constant
                                              , cci_avg_length
                                              , long_cci_ratio, short_cci_ratio))
        else:
            cci_period_ary = [i for i in range(5, 20, 5)]
            cci_constant_ary = [0.015]
            cci_avg_length_ary = [i for i in range(3, 25, 5)]
            long_cci_ratio_ary = [-60, -80, -100]
            short_cci_ratio_ary = [60, 80, 100]
            for cci_period in cci_period_ary:
                for cci_constant in cci_constant_ary:
                    for cci_avg_length in cci_avg_length_ary:
                        for long_cci_ratio in long_cci_ratio_ary:
                            for short_cci_ratio in short_cci_ratio_ary:
                                strategies.append(EntryCommodityChannelIndex(ohlcv
                                                                             , cci_period
                                                                             , cci_constant
                                                                             , cci_avg_length
                                                                             , long_cci_ratio
                                                                             , short_cci_ratio))
        return strategies


class EntryCommodityChannelIndex(EntryStrategy):
    """
    CCIの平均が基準値を超えていればエントリーする
    """

    def __init__(self
                 , ohlcv
                 , cci_period
                 , cci_constant
                 , cci_avg_length
                 , long_cci_ratio=-100
                 , short_cci_ratio=100
                 , order_vol_ratio=0.01):
        self.title = f"CCI[{cci_period:.0f},{cci_constant:.3f},{cci_avg_length:.0f}][{long_cci_ratio:.0f},{short_cci_ratio:.0f}]"
        self.ohlcv = ohlcv
        self.symbol = self.ohlcv.symbol
        self.cci = CommodityChannelIndex(ohlcv, cci_period, cci_constant)
        self.cci_avg_length = cci_avg_length
        self.long_cci_ratio = long_cci_ratio
        self.short_cci_ratio = short_cci_ratio
        self.order_vol_ratio = order_vol_ratio
        s = self.cci.cci
        self.cci_sma = s.rolling(window=self.cci_avg_length).mean()

    def _is_indicator_valid(self, idx):
        if (
                self.cci.cci[idx] == 0
        ):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        """
        当日CCIの平均値が基準値を下回っていればロング
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        cci_avg_value = self.cci_sma[idx]
        if cci_avg_value <= self.long_cci_ratio:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        当日CCIの平均値が基準値を上回っていればショート
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        cci_avg_value = self.cci_sma[idx]
        if cci_avg_value >= self.short_cci_ratio:
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
        ind1 = self.cci.cci[idx]
        ind2 = self.long_cci_ratio
        ind3 = self.short_cci_ratio
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

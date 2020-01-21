import math
import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.average_true_range import AverageTrueRange
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class AsymmetricAgainWithFlowFactory(EntryStrategyFactory):
    params = {
        # atr_span, atr_mult
        "default": [15, 0.5]
        , "^N225": [10, 0.5]
        , "3288.T": [15, 0.5]
        , "4043.T": [15, 0.5]
        , "3038.T": [20, 0.3]
        , "7974.T": [10, 0.5]
        # , "9104.T": [20, 0.3]
        , "9104.T": [10, 0.3]
        , "5706.T": [5, 0.7]
        , "4523.T": [15, 0.5]
        , "2412.T": [5, 0.5]
        , "9983.T": [15, 0.5]
        , "8876.T": [5, 0.5]
        , "4911.T": [10, 0.5]
        , "8267.T": [20, 0.9]
        , "4967.T": [20, 0.7]
        , "6141.T": [5, 0.3]
        , "5713.T": [15, 0.5]
        , "1802.T": [15, 0.7]
        , "3141.T": [5, 0.7]
        # , "9007.T": [20, 1.1]
    }

    def create(self, ohlcv, optimization=False):
        strategies = []
        if not optimization:
            #
            s = ohlcv.symbol
            if s in self.params:
                atr_span = self.params[s][0]
                atr_mult = self.params[s][1]
            else:
                atr_span = self.params["default"][0]
                atr_mult = self.params["default"][1]
            strategies.append(AsymmetricAgainWithFlow(ohlcv, atr_span, atr_mult))
        else:
            atr_spans = [i for i in range(5, 25, 5)]
            atr_mults = [i for i in np.arange(0.3, 1.5, 0.2)]
            for atr_span in atr_spans:
                for atr_mult in atr_mults:
                    strategies.append(AsymmetricAgainWithFlow(ohlcv, atr_span, atr_mult))
        return strategies


class AsymmetricAgainWithFlow(EntryStrategy):
    """
    前日安値でエントリーを判定し、ATRを用いて逆指値注文する
    """
    def __init__(self
                 , ohlcv
                 , atr_span
                 , atr_mult
                 , order_vol_ratio=0.01):
        self.title = f"AsymmetricAgainWithFlow[{atr_span:.0f},{atr_mult:.2f}]"
        self.ohlcv = ohlcv
        self.atr = AverageTrueRange(ohlcv, atr_span)
        self.atr_mult = atr_mult
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.atr.atr[idx] == 0
        ):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        """
        前日安値が当日始値よりも安い場合は逆指値でロングのエントリー
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.atr.atr_span:
            return OrderType.NONE_ORDER
        momentum = self.ohlcv.values['close'][idx] - self.ohlcv.values['close'][idx - self.atr.atr_span]
        value1 = self.ohlcv.values['open'][idx]
        value2 = self.ohlcv.values['low'][idx-1]
        if not np.isnan(value1) and not np.isnan(value2) and (value1 >= value2 and momentum > 0):
            return OrderType.STOP_MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        前日安値が当日始値よりも高い場合は逆指値でショートのエントリー
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.atr.atr_span:
            return OrderType.NONE_ORDER
        momentum = self.ohlcv.values['close'][idx] - self.ohlcv.values['close'][idx - self.atr.atr_span]
        value1 = self.ohlcv.values['open'][idx]
        value2 = self.ohlcv.values['low'][idx-1]
        if np.isnan(value1) or np.isnan(value2) or (value1 >= value2 and momentum < 0):
            return OrderType.NONE_ORDER
        else:
            # return OrderType.NONE_ORDER
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
        price = math.ceil(close + self.atr_mult * self.atr.atr[idx])
        return price

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        low = self.ohlcv.values['low'][idx]
        price = math.floor(low - self.atr_mult * self.atr.atr[idx])
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
        ind1 = self.ohlcv.values['close'][idx] + self.atr.atr[idx] * self.atr_mult
        ind2 = self.ohlcv.values['low'][idx] - self.atr.atr[idx] * self.atr_mult
        ind3 = self.atr.atr[idx]
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7


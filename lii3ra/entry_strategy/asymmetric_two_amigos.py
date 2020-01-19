import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.average_true_range import AverageTrueRange
from lii3ra.technical_indicator.average_directional_index import AverageDirectionalIndex
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class AsymmetricTwoAmigosFactory(EntryStrategyFactory):
    params = {
        # atr_span, atr_mult, adx_span, adx_threshold
        "default": [15, 0.5, 14, 0.20]
        , "^N225": [18, 0.7, 3, 0.00]
        , "1570.T": [3, 0.5, 3, 0.60]
    }

    rough_params = [
        [10, 0.5, 14, 0.20]
        , [15, 0.5, 14, 0.20]
        , [20, 0.5, 14, 0.20]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            atr_span = self.params[s][0]
            atr_mult = self.params[s][1]
            adx_span = self.params[s][2]
            adx_threshold = self.params[s][3]
        else:
            atr_span = self.params["default"][0]
            atr_mult = self.params["default"][1]
            adx_span = self.params["default"][2]
            adx_threshold = self.params["default"][3]
        return AsymmetricTwoAmigos(ohlcv, atr_span, atr_mult, adx_span, adx_threshold)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            #
            for p in self.rough_params:
                strategies.append(AsymmetricTwoAmigos(ohlcv
                                                      , p[0]
                                                      , p[1]
                                                      , p[2]
                                                      , p[3]))
        else:
            atr_span_list = [i for i in range(3, 20, 3)]
            atr_mult_list = [i for i in np.arange(0.3, 1.5, 0.2)]
            adx_span_list = [i for i in range(3, 20, 3)]
            adx_threshold_list = [i for i in np.arange(0.0, 1.0, 0.2)]
            for atr_span in atr_span_list:
                for atr_mult in atr_mult_list:
                    for adx_span in adx_span_list:
                        for adx_threshold in adx_threshold_list:
                            strategies.append(AsymmetricTwoAmigos(ohlcv, atr_span, atr_mult, adx_span, adx_threshold))
        return strategies


class AsymmetricTwoAmigos(EntryStrategy):
    """
    前日安値でエントリーを判定し、ATRを用いて逆指値注文する
    """
    def __init__(self
                 , ohlcv
                 , atr_span
                 , atr_mult
                 , adx_span
                 , adx_threshold
                 , order_vol_ratio=0.01):
        self.title = f"AsymmetricTwoAmigos[{atr_span:.0f},{atr_mult:.2f}][{adx_span:.0f},{adx_threshold:.2f}]"
        self.ohlcv = ohlcv
        self.atr = AverageTrueRange(ohlcv, atr_span)
        self.atr_mult = atr_mult
        self.adx = AverageDirectionalIndex(ohlcv, adx_span)
        self.adx_threshold = adx_threshold
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
        if idx <= self.adx.adx_span:
            return OrderType.NONE_ORDER
        if self.adx.adx[idx] > self.adx_threshold:
            value1 = self.ohlcv.values['open'][idx]
            value2 = self.ohlcv.values['low'][idx-1]
            if not np.isnan(value1) and not np.isnan(value2) and value1 >= value2:
                return OrderType.STOP_MARKET_LONG
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
        if idx <= self.adx.adx_span:
            return OrderType.NONE_ORDER
        if self.adx.adx[idx] > self.adx_threshold:
            value1 = self.ohlcv.values['open'][idx]
            value2 = self.ohlcv.values['low'][idx-1]
            if np.isnan(value1) or np.isnan(value2) or value1 >= value2:
                return OrderType.NONE_ORDER
            else:
                return OrderType.STOP_MARKET_SHORT
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
        close = self.ohlcv.values['close'][idx]
        price = close + self.atr_mult * self.atr.atr[idx]
        return price

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        low = self.ohlcv.values['low'][idx]
        price = low - self.atr_mult * self.atr.atr[idx]
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
        ind4 = self.adx.adx[idx]
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7


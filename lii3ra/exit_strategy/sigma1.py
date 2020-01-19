import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.bollingerband import Bollingerband
from lii3ra.exit_strategy.exit_strategy import ExitStrategyFactory
from lii3ra.exit_strategy.exit_strategy import ExitStrategy


class Sigma1Factory(ExitStrategyFactory):
    params = {
        # span, sigma1_ratio
        "default": [3, 1.0]
    }

    rough_params = [
        [3, 1.0]
        , [6, 1.0]
        , [9, 1.0]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            span = self.params[s][0]
            sigma1_ratio = self.params[s][1]
        else:
            span = self.params["default"][0]
            sigma1_ratio = self.params["default"][1]
        return Sigma1(ohlcv
                      , span
                      , sigma1_ratio)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            for p in self.rough_params:
                strategies.append(Sigma1(ohlcv, p[0], p[1], p[2], p[3], p[4]))
        else:
            long_span_list = [5, 10, 15, 20]
            long_ratio_list = [30, 40, 50, 60, 70]
            short_span_list = [5, 10, 15, 20]
            short_ratio_list = [30, 40, 50, 60, 70]
            losscut_ratio_list = [0.05]
            for long_span in long_span_list:
                for long_ratio in long_ratio_list:
                    for short_span in short_span_list:
                        for short_ratio in short_ratio_list:
                            for losscut_ratio in losscut_ratio_list:
                                strategies.append(Sigma1(ohlcv
                                                         , long_span
                                                         , long_ratio
                                                         , short_span
                                                         , short_ratio
                                                         , losscut_ratio))
        return strategies


class Sigma1(ExitStrategy):
    """
    BollingerBandによる逆指値
    """

    # TODO:逆指値しない。終値がBandを超えていたら次のバーでEXIT
    def __init__(self
                 , ohlcv
                 , span
                 , sigma1_ratio
                 , losscut_ratio=0.05):
        self.title = f"Sigma1[{span:.0f},{sigma1_ratio:.2f}]"
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol
        self.bb = Bollingerband(ohlcv, span, sigma1_ratio)
        self._last_price = 0
        self.pos_price = 0
        self.losscut_ratio = losscut_ratio

    def check_exit_long(self, pos_price, pos_vol, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.bb.sma_span:
            return OrderType.NONE_ORDER
        self.pos_price = pos_price
        return OrderType.CLOSE_LONG_STOP_MARKET

    def check_exit_short(self, pos_price, pos_vol, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.bb.sma_span:
            return OrderType.NONE_ORDER
        self.pos_price = pos_price
        return OrderType.CLOSE_SHORT_STOP_MARKET

    def create_order_exit_long_stop_market(self, idx, entry_idx):
        if not self._is_valid(idx):
            return 0.00
        price = self.bb.lower_sigma1[idx]
        # 最低losscut設定
        losscut_price = self.pos_price - (self.pos_price * self.losscut_ratio)
        if price < losscut_price:
            price = losscut_price
        return price

    def create_order_exit_short_stop_market(self, idx, entry_idx):
        if not self._is_valid(idx):
            return 0.00
        price = self.bb.upper_sigma1[idx]
        # 最低losscut設定
        losscut_price = self.pos_price + (self.pos_price * self.losscut_ratio)
        if price > losscut_price:
            price = losscut_price
        return price

    def create_order_exit_long_market(self, idx, entry_idx):
        return 0.00

    def create_order_exit_short_market(self, idx, entry_idx):
        return 0.00

    def get_indicators(self, idx, entry_idx):
        ind1 = self._last_price
        ind2 = None
        ind3 = None
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        self._last_price = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

import math
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

    def create(self, ohlcv, optimization=False):
        strategies = []
        if not optimization:
            #
            s = ohlcv.symbol
            if s in self.params:
                span = self.params[s][0]
                sigma1_ratio = self.params[s][1]
            else:
                span = self.params["default"][0]
                sigma1_ratio = self.params["default"][1]
            strategies.append(Sigma1(ohlcv
                                     , span
                                     , sigma1_ratio))
        else:
            span_list = [i for i in range(3, 25, 5)]
            sigma1_ratio_list = [0.1, 0.2, 0.3, 0.6, 0.9, 1.2, 1.5]
            losscut_ratio_list = [0.03, 0.05]
            for span in span_list:
                for sigma1_ratio in sigma1_ratio_list:
                    for losscut_ratio in losscut_ratio_list:
                        strategies.append(Sigma1(ohlcv
                                                 , span
                                                 , sigma1_ratio
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
                 , num_of_bars_long
                 , num_of_bars_short
                 , losscut_ratio=0.05):
        self.title = f"Sigma1[{span:.0f},{sigma1_ratio:.2f}][{num_of_bars_long:0.f},{num_of_bars_short:.0f}]"
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol
        self.bb = Bollingerband(ohlcv, span, sigma1_ratio)
        self.sigma1_ratio = sigma1_ratio
        self.num_of_bars_long = num_of_bars_long
        self.num_of_bars_short = num_of_bars_short
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
        # price = self.bb.lower_sigma1[idx]
        num_of_bars = idx - entry_idx
        price = self.bb.sma - (self.sigma[idx] * self.sigma1_ratio / num_of_bars)
        # 最低losscut設定
        losscut_price = self.pos_price - (self.pos_price * self.losscut_ratio)
        if price < losscut_price:
            price = losscut_price
        return math.floor(price)

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

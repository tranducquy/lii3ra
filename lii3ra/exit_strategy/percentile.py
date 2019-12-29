import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.simple_movingaverage import SimpleMovingAverage
from lii3ra.exit_strategy.exit_strategy import ExitStrategyFactory
from lii3ra.exit_strategy.exit_strategy import ExitStrategy


class PercentileFactory(ExitStrategyFactory):
    params = {
        # percentile_span_long, percentile_ratio_long, percentile_span_short, percentile_span_short, percentile_ratio_short, percentile_losscut_ratio
        "default": [5, 50, 5, 50, 0.10]
    }

    rough_params = [
        [5, 50, 5, 50, 0.10]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            long_span = self.params[s][0]
            long_ratio = self.params[s][1]
            short_span = self.params[s][2]
            short_ratio = self.params[s][3]
            losscut_ratio = self.params[s][4]
        else:
            long_span = self.params["default"][0]
            long_ratio = self.params["default"][1]
            short_span = self.params["default"][2]
            short_ratio = self.params["default"][3]
            losscut_ratio = self.params["default"][4]
        return Percentile(ohlcv
                          , long_span
                          , long_ratio
                          , short_span
                          , short_ratio
                          , losscut_ratio)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            for p in self.rough_params:
                strategies.append(Percentile(ohlcv, p[0], p[1], p[2], p[3], p[4]))
        else:
            long_span_list = [5, 10, 15]
            long_ratio_list = [0.40, 0.50, 0.60]
            short_span_list = [5, 10, 15]
            short_ratio_list = [0.40, 0.50, 0.60]
            losscut_ratio_list = [0.03, 0.05, 0.10]
            for long_span in long_span_list:
                for long_ratio in long_ratio_list:
                    for short_span in short_span_list:
                        for short_ratio in short_ratio_list:
                            for losscut_ratio in losscut_ratio_list:
                                strategies.append(Percentile(ohlcv
                                                             , long_span
                                                             , long_ratio
                                                             , short_span
                                                             , short_ratio
                                                             , losscut_ratio))
        return strategies


class Percentile(ExitStrategy):
    """
    指定したバーのパーセンタイルで逆指値返済注文する
    """

    # TODO:逆指値しない
    def __init__(self
                 , ohlcv
                 , long_span
                 , long_ratio
                 , short_span
                 , short_ratio
                 , losscut_ratio=0.05):
        self.title = f"Percentile[{long_span:.0f},{long_ratio:.2f}][{short_span:.0f},{short_ratio:.2f}][{losscut_ratio:.2f}]"
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol
        self.percentile_span_long = long_span
        self.percentile_ratio_long = long_ratio
        self.percentile_span_short = short_span
        self.percentile_ratio_short = short_ratio
        self._last_price = 0
        self.pos_price = 0
        self.losscut_ratio = losscut_ratio

    def check_exit_long(self, pos_price, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        self.pos_price = pos_price
        return OrderType.CLOSE_LONG_STOP_MARKET

    def check_exit_short(self, pos_price, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        self.pos_price = pos_price
        return OrderType.CLOSE_SHORT_STOP_MARKET

    def create_order_exit_long_stop_market(self, idx, entry_idx):
        if not self._is_valid(idx):
            return 0.00
        # 指定したバー内でのパーセンタイル取得
        price = self._calc_percentile(idx, self.percentile_span_long, self.percentile_ratio_long)
        # 最低losscut設定
        losscut_price = self.pos_price - (self.pos_price * self.losscut_ratio)
        if price < losscut_price:
            price = losscut_price
        return price

    def create_order_exit_short_stop_market(self, idx, entry_idx):
        if not self._is_valid(idx):
            return 0.00
        # 指定したバー内でのパーセンタイル取得
        price = self._calc_percentile(idx, self.percentile_span_short, self.percentile_ratio_short)
        # 最低losscut設定
        losscut_price = self.pos_price + (self.pos_price * self.losscut_ratio)
        if price > losscut_price:
            price = losscut_price
        return price

    def create_order_exit_long_market(self, idx, entry_idx):
        return 0.00

    def create_order_exit_short_market(self, idx, entry_idx):
        return 0.00

    def _calc_percentile(self, idx, span, q):
        org = idx - span + 1 if idx - span > 0 else idx
        prices = self.ohlcv.values['close'][org:idx + 1]
        self._last_price = np.nanpercentile(prices, q)
        return self._last_price

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

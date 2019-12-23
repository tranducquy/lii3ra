import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.exit_strategy.exit_strategy import ExitStrategy


class Percentile(ExitStrategy):
    """
    指定したバーのパーセンタイルで逆指値返済注文する
    """

    # TODO:逆指値しない
    def __init__(self
                 , title
                 , ohlcv
                 , percentile_span_long
                 , percentile_ratio_long
                 , percentile_span_short
                 , percentile_ratio_short
                 , losscut_ratio=0.03):
        self.title = title
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol
        self.percentile_span_long = percentile_span_long
        self.percentile_ratio_long = percentile_ratio_long
        self.percentile_span_short = percentile_span_short
        self.percentile_ratio_short = percentile_ratio_short
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

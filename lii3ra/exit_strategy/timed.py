from lii3ra.ordertype import OrderType
from lii3ra.exit_strategy.exit_strategy import ExitStrategy


class Timed(ExitStrategy):
    """
    指定したバーが経過したら成行返済する。
    Entryした次のバーで返済する場合はnum_of_barsに1を設定する。
    """
    def __init__(self, title, ohlcv, imethod=1, num_of_bars_long=3, num_of_bars_short=3, losscut_ratio=0.03):
        self.title = title
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol
        self.imethod = imethod
        self.num_of_bars_long = num_of_bars_long
        self.num_of_bars_short = num_of_bars_short
        self.losscut_ratio = losscut_ratio

    def check_exit_long(self, pos_price, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        # exit after specified number of bars
        if self.imethod == 1:
            if idx >= entry_idx + self.num_of_bars_long - 1:
                return OrderType.CLOSE_LONG_MARKET
        # exit after specified number of bars, ONLY if position is currently porofitable
        elif self.imethod == 2:
            if (idx >= entry_idx + self.num_of_bars_long - 1
                    and pos_price < self.ohlcv.values['close'][idx]):
                return OrderType.CLOSE_LONG_MARKET
        # exit after specified number of bars, ONLY if position is currently losing
        elif self.imethod == 3:
            if (idx >= entry_idx + self.num_of_bars_long - 1
                    and pos_price > self.ohlcv.values['close'][idx]):
                return OrderType.CLOSE_LONG_MARKET
        # ロスカット
        close = self.ohlcv.values['close'][idx]
        losscut_price = pos_price - (pos_price * self.losscut_ratio)
        if close < losscut_price:
            return OrderType.CLOSE_LONG_MARKET
        else:
            return OrderType.NONE_ORDER

    def check_exit_short(self, pos_price, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        # exit after specified number of bars
        if self.imethod == 1:
            if idx >= entry_idx + self.num_of_bars_short - 1:
                return OrderType.CLOSE_SHORT_MARKET
        # exit after specified number of bars, ONLY if position is currently porofitable
        elif self.imethod == 2:
            if (idx >= entry_idx + self.num_of_bars_short - 1
                    and pos_price > self.ohlcv.values['close'][idx]):
                return OrderType.CLOSE_SHORT_MARKET
        # exit after specified number of bars, ONLY if position is currently losing
        elif self.imethod == 3:
            if (idx >= entry_idx + self.num_of_bars_short - 1
                    and pos_price < self.ohlcv.values['close'][idx]):
                return OrderType.CLOSE_SHORT_MARKET
        # ロスカット
        close = self.ohlcv.values['close'][idx]
        losscut_price = pos_price + (pos_price * self.losscut_ratio)
        if close > losscut_price:
            return OrderType.CLOSE_SHORT_MARKET
        else:
            return OrderType.NONE_ORDER

    def create_order_exit_long_stop_market(self, idx, entry_idx):
        if not self._is_valid(idx):
            return 0.00
        # dummy
        price = self.ohlcv.values['close'][idx]
        return price

    def create_order_exit_short_stop_market(self, idx, entry_idx):
        if not self._is_valid(idx):
            return 0.00
        # dummy
        price = self.ohlcv.values['close'][idx]
        return price

    def create_order_exit_long_market(self, idx, entry_idx):
        return 0.00

    def create_order_exit_short_market(self, idx, entry_idx):
        return 0.00

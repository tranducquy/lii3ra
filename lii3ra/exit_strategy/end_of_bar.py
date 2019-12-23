from lii3ra.ordertype import OrderType
from lii3ra.exit_strategy.exit_strategy import ExitStrategy


class EndOfBar(ExitStrategy):
    """
    Entryしたバーの終値で成行返済する。実装はmarket.py
    """
    def __init__(self, title, ohlcv):
        self.title = title
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol

    def check_exit_long(self, pos_price, idx, entry_idx):
        return OrderType.NONE_ORDER

    def check_exit_short(self, pos_price, idx, entry_idx):
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


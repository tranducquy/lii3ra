from lii3ra.ordertype import OrderType
from lii3ra.exit_strategy.exit_strategy import ExitStrategy


class TimedByTime(ExitStrategy):
    """
    指定した時刻に成行返済する。
    分足および秒足のみ対応
    """
    def __init__(self, title, ohlcv, exit_time, losscut_ratio=0.03):
        self.title = title
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol
        self.exit_time = exit_time
        self.losscut_ratio = losscut_ratio

    def check_exit_long(self, pos_price, pos_vol, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        current_time = self.ohlcv.values['time'][idx].strftime("%H%M%S")
        if current_time >= self.exit_time:
            return OrderType.CLOSE_LONG_MARKET
        # ロスカット
        close = self.ohlcv.values['close'][idx]
        losscut_price = pos_price - (pos_price * self.losscut_ratio)
        if close < losscut_price:
            return OrderType.CLOSE_LONG_MARKET
        else:
            return OrderType.NONE_ORDER

    def check_exit_short(self, pos_price, pos_vol, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        current_time = self.ohlcv.values['time'][idx].strftime("%H%M%S")
        if current_time >= self.exit_time:
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


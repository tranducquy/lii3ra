from lii3ra.ordertype import OrderType
from lii3ra.tick import Tick
from lii3ra.exit_strategy.exit_strategy import ExitStrategyFactory
from lii3ra.exit_strategy.exit_strategy import ExitStrategy


class NewvalueFactory(ExitStrategyFactory):

    def create_strategy(self, ohlcv):
        return Newvalue(ohlcv)

    def optimization_rough(self, ohlcv):
        strategies = [Newvalue(ohlcv)]
        return strategies

    def optimization(self, ohlcv):
        strategies = [Newvalue(ohlcv)]
        return strategies


class Newvalue(ExitStrategy):
    """直前のバーの高値または安値に1tick加算または減算した価格で逆指値注文する"""
    def __init__(self, ohlcv):
        self.title = "NewValue"
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol
        self.tick = Tick.get_tick(self.symbol)
    
    def check_exit_long(self, pos_price, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx < 1:
            return OrderType.NONE_ORDER
        return OrderType.CLOSE_LONG_STOP_MARKET

    def check_exit_short(self, pos_price, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx < 1:
            return OrderType.NONE_ORDER
        return OrderType.CLOSE_SHORT_STOP_MARKET

    def create_order_exit_long_stop_market(self, idx, entry_idx):
        if not self._is_valid(idx):
            return 0.00
        # 前のバーの安値取得
        price = self.ohlcv.values['low'][idx - 1]
        price -= self.tick
        return price

    def create_order_exit_short_stop_market(self, idx, entry_idx):
        if not self._is_valid(idx):
            return 0.00
        # 前のバーの高値取得
        price = self.ohlcv.values['high'][idx - 1]
        price += self.tick
        return price

    def create_order_exit_long_market(self, idx, entry_idx):
        return 0.00

    def create_order_exit_short_market(self, idx, entry_idx):
        return 0.00


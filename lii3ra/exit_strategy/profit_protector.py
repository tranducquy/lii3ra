from lii3ra.ordertype import OrderType
from lii3ra.exit_strategy.exit_strategy import ExitStrategy


class ProfitProtector(ExitStrategy):
    """
    ポジションの最大利益がprofit_floorより大きい場合に、
    現在のポジションの利益を最大利益で割った値がpp_ratioより小さい場合、次のバーで成行返済する。
    """

    def __init__(self, title, ohlcv, long_profit_floor, long_pp_ratio, short_profit_floor, short_pp_ratio):
        self.title = title
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol
        self.long_profit_floor = long_profit_floor
        self.long_pp_ratio = long_pp_ratio
        self.short_profit_floor = short_profit_floor
        self.short_pp_ratio = short_pp_ratio
        self.max_profit = 0

    def check_exit_long(self, pos_price, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx == entry_idx:
            self.current_profit = 0
            self.max_profit = 0
        close = self.ohlcv.values['close'][idx]
        self.current_profit = close - pos_price
        self.max_profit = self.current_profit if self.max_profit < self.current_profit else self.max_profit
        if self.max_profit >= self.long_profit_floor:
            if (self.current_profit / self.max_profit) < self.long_pp_ratio:
                return OrderType.CLOSE_LONG_MARKET
        return OrderType.NONE_ORDER

    def check_exit_short(self, pos_price, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx == entry_idx:
            self.current_profit = 0
            self.max_profit = 0
        close = self.ohlcv.values['close'][idx]
        self.current_profit = pos_price - close
        self.max_profit = self.current_profit if self.max_profit < self.current_profit else self.max_profit
        if self.max_profit >= self.short_profit_floor:
            if (self.current_profit / self.max_profit) < self.short_pp_ratio:
                return OrderType.CLOSE_SHORT_MARKET
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

    def get_indicators(self, idx, entry_idx):
        ind1 = self.max_profit
        ind2 = self.current_profit
        ind3 = (self.current_profit / self.max_profit)
        ind4 = self.long_profit_floor
        ind5 = self.long_pp_ratio
        ind6 = self.short_profit_floor
        ind7 = self.short_pp_ratio
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

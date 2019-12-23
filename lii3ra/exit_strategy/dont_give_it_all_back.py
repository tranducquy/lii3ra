from lii3ra.ordertype import OrderType
from lii3ra.exit_strategy.exit_strategy import ExitStrategy


class DontGiveItAllBack(ExitStrategy):
    """
    最大含み益と現在の含み益の差がxATR*ATRよりも大きい場合、次のバーで成行でクローズする。
    """
    def __init__(self, title, ohlcv, long_atr, short_atr, long_xatr=0.2, short_xatr=0.2):
        self.title = title
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol
        self.long_atr = long_atr
        self.short_atr = short_atr
        self.long_xatr = long_xatr
        self.short_xatr = short_xatr
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
        self.profit_diff = self.max_profit - self.current_profit
        if self.profit_diff > self.long_atr.atr[idx] * self.long_xatr:
            return OrderType.CLOSE_LONG_MARKET
        else:
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
        self.profit_diff = self.max_profit - self.current_profit
        if self.profit_diff > self.short_atr.atr[idx] * self.short_xatr:
            return OrderType.CLOSE_SHORT_MARKET
        else:
            return OrderType.NONE_ORDER

    def create_order_exit_long_stop_market(self, idx, entry_idx):
        if not self._is_valid(idx):
            return 0.00
        #dummy
        price = self.ohlcv.values['close'][idx]
        return price

    def create_order_exit_short_stop_market(self, idx, entry_idx):
        if not self._is_valid(idx):
            return 0.00
        #dummy
        price = self.ohlcv.values['close'][idx]
        return price

    def create_order_exit_long_market(self, idx, entry_idx):
        return 0.00

    def create_order_exit_short_market(self, idx, entry_idx):
        return 0.00

    def get_indicators(self, idx, entry_idx):
        ind1 = self.long_atr.atr[idx]
        ind2 = (self.long_atr.atr[idx] * self.long_xatr) 
        ind3 = self.short_atr.atr[idx]
        ind4 = (self.short_atr.atr[idx] * self.short_xatr) 
        ind5 = self.max_profit if hasattr(self, "max_profit") else None
        ind6 = self.current_profit if hasattr(self, "current_profit") else None
        ind7 = self.profit_diff if hasattr(self, "profit_diff") else None
        return (ind1, ind2, ind3, ind4, ind5, ind6, ind7)

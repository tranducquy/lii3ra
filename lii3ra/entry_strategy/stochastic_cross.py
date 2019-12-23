from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class StochasticCross(EntryStrategy):
    """
    ％kと％dのクロスでエントリー。
    """

    def __init__(self
                 , title
                 , ohlcv
                 , stoch
                 , order_vol_ratio=0.01):
        self.title = title
        self.ohlcv = ohlcv
        self.symbol = self.ohlcv.symbol
        self.stoch = stoch
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.stoch.fast_k[idx] == 0
                or self.stoch.fast_d[idx] == 0
                or self.stoch.slow_k[idx] == 0
                or self.stoch.slow_d[idx] == 0
        ):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        """
        slow kがslow d を上回ったら次で成行ロング
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx < self.stoch.period:
            return OrderType.NONE_ORDER
        before_condition = self.stoch.slow_k[idx-1] < self.stoch.slow_d[idx-1]
        current_condition = self.stoch.slow_k[idx] > self.stoch.slow_d[idx]
        if before_condition and current_condition:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        slow kがslow d を下回ったら次で成行ショート
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx < self.stoch.period:
            return OrderType.NONE_ORDER
        before_condition = self.stoch.slow_k[idx-1] > self.stoch.slow_d[idx-1]
        current_condition = self.stoch.slow_k[idx] < self.stoch.slow_d[idx]
        if before_condition and current_condition:
            return OrderType.MARKET_SHORT
        else:
            return OrderType.NONE_ORDER

    def create_order_entry_long_stop_market_for_all_cash(self, cash, idx, last_exit_idx):
        if not self._is_valid(idx) or cash <= 0:
            return -1, -1
        price = self.create_order_entry_long_stop_market(idx, last_exit_idx)
        vol = self.get_order_vol(cash, idx, price, last_exit_idx)
        return price, vol

    def create_order_entry_short_stop_market_for_all_cash(self, cash, idx, last_exit_idx):
        if not self._is_valid(idx) or cash <= 0:
            return -1, -1
        price = self.create_order_entry_short_stop_market(idx, last_exit_idx)
        vol = self.get_order_vol(cash, idx, price, last_exit_idx)
        return price, vol * -1

    def create_order_entry_long_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        return 0.00

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        return 0.00

    def create_order_entry_long_market_for_all_cash(self, cash, idx, last_exit_idx):
        if not self._is_valid(idx) or cash <= 0:
            return -1, -1
        price = self.ohlcv.values['close'][idx]
        vol = self.get_order_vol(cash, idx, price, last_exit_idx)
        return price, vol

    def create_order_entry_short_market_for_all_cash(self, cash, idx, last_exit_idx):
        if not self._is_valid(idx) or cash <= 0:
            return -1, -1
        price = self.ohlcv.values['close'][idx]
        vol = self.get_order_vol(cash, idx, price, last_exit_idx)
        return price, vol * -1

    def get_indicators(self, idx, last_exit_idx):
        ind1 = self.stoch.fast_k[idx]
        ind2 = self.stoch.fast_d[idx]
        ind3 = self.stoch.slow_k[idx]
        ind4 = self.stoch.slow_d[idx]
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class NewHighWithConsecutiveHighs(EntryStrategy):
    """
    最高値または最安値が連続して更新されたらエントリーする
    """

    def __init__(self
                 , title
                 , ohlcv
                 , long_lookback_period
                 , long_consecutive_cnt
                 , short_lookback_period
                 , short_consecutive_cnt
                 , order_vol_ratio=0.01):
        self.title = title
        self.ohlcv = ohlcv
        self.long_lookback_period = long_lookback_period
        self.long_consecutive_cnt = long_consecutive_cnt
        self.short_lookback_period = short_lookback_period
        self.short_consecutive_cnt = short_consecutive_cnt
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def check_entry_long(self, idx, last_exit_idx):
        """
        最高値が連続して更新されたらエントリーする
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.long_lookback_period:
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        lookback_period = self.long_lookback_period
        high_values = self.ohlcv.values['high'][idx - lookback_period:idx]
        close_values = self.ohlcv.values['close'][idx - lookback_period:idx]
        cnt = self.long_consecutive_cnt
        for c in range(1, cnt + 1):
            consecutive_flg = close_values[idx - c] > close_values[idx - c - 1]
            if not consecutive_flg:
                return OrderType.NONE_ORDER
        max_high = high_values.max()
        long_condition = close > max_high
        if long_condition:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        最安値が連続して更新されたらエントリーする
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.short_lookback_period:
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        lookback_period = self.short_lookback_period
        low_values = self.ohlcv.values['low'][idx - lookback_period:idx]
        close_values = self.ohlcv.values['close'][idx - lookback_period:idx]
        cnt = self.short_consecutive_cnt
        for c in range(1, cnt + 1):
            consecutive_flg = close_values[idx - c] < close_values[idx - c - 1]
            if not consecutive_flg:
                return OrderType.NONE_ORDER
        min_low = low_values.min()
        short_condition = close < min_low
        if short_condition:
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
        ind1 = None
        ind2 = None
        ind3 = None
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

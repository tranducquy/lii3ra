from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class BreakoutWithTwist(EntryStrategy):
    """
    高値または安値が指定のバー数の高値を更新した場合に成行注文する
    """

    def __init__(self
                 , title
                 , ohlcv
                 , long_lookback_span
                 , long_adx_value
                 , long_adx
                 , short_lookback_span
                 , short_adx_value
                 , short_adx
                 , order_vol_ratio=0.01):
        self.title = title
        self.ohlcv = ohlcv
        self.long_lookback_span = long_lookback_span
        self.long_adx_value = long_adx_value
        self.long_adx = long_adx
        self.short_lookback_span = short_lookback_span
        self.short_adx_value = short_adx_value
        self.short_adx = short_adx
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.long_adx.adx[idx] == 0
                or self.short_adx.adx[idx] == 0
        ):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        # 当日高値が指定バー数分の高値を更新した場合、次のバーで成行買
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        max_high = self.ohlcv.values['high'][idx - self.long_lookback_span:idx].max()
        long_flg = max_high < self.ohlcv.values['high'][idx]
        long_adx_flg = self.long_adx.adx[idx] < self.long_adx_value
        if long_flg and long_adx_flg:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        # 当日安値が指定バー数分の安値を更新した場合、次のバーで成行売
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        min_low = self.ohlcv.values['low'][idx - self.short_lookback_span:idx].min()
        short_flg = min_low > self.ohlcv.values['low'][idx]
        short_adx_flg = self.short_adx.adx[idx] < self.short_adx_value
        if short_flg and short_adx_flg:
            return OrderType.MARKET_SHORT
        else:
            return OrderType.NONE_ORDER

    def create_order_entry_long_stop_market_for_all_cash(self, cash, idx, last_exit_idx):
        if not self._is_valid(idx) or cash <= 0:
            return (-1, -1)
        price = self.create_order_entry_long_stop_market(idx, last_exit_idx)
        vol = self.get_order_vol(cash, idx, price, last_exit_idx)
        return (price, vol)

    def create_order_entry_short_stop_market_for_all_cash(self, cash, idx, last_exit_idx):
        if not self._is_valid(idx) or cash <= 0:
            return (-1, -1)
        price = self.create_order_entry_short_stop_market(idx, last_exit_idx)
        vol = self.get_order_vol(cash, idx, price, last_exit_idx)
        return (price, vol * -1)

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
            return (-1, -1)
        price = self.ohlcv.values['close'][idx]
        vol = self.get_order_vol(cash, idx, price, last_exit_idx)
        return (price, vol)

    def create_order_entry_short_market_for_all_cash(self, cash, idx, last_exit_idx):
        if not self._is_valid(idx) or cash <= 0:
            return (-1, -1)
        price = self.ohlcv.values['close'][idx]
        vol = self.get_order_vol(cash, idx, price, last_exit_idx)
        return (price, vol * -1)

    def get_indicators(self, idx, last_exit_idx):
        ind1 = self.long_adx.adx[idx]
        ind2 = self.long_adx_value
        ind3 = self.long_lookback_span
        ind4 = self.short_adx.adx[idx]
        ind5 = self.short_adx_value
        ind6 = self.short_lookback_span
        ind7 = None
        return (ind1, ind2, ind3, ind4, ind5, ind6, ind7)

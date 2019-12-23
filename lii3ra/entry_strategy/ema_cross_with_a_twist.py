from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class EMACrossWithTwist(EntryStrategy):
    """
    指数平滑移動平均の短期と長期を用いて移動平均のクロスと、指定の閾値を比較し、次のバーで成行エントリーする
    """

    def __init__(self
                 , title
                 , ohlcv
                 , fast_ema
                 , slow_ema
                 , price_threshold
                 , order_vol_ratio=0.01):
        self.title = title
        self.ohlcv = ohlcv
        self.fast_ema = fast_ema
        self.slow_ema = slow_ema
        self.price_threshold = price_threshold
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.fast_ema.ema[idx] == 0
                or self.slow_ema.ema[idx] == 0
        ):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        """
        短期EMAが長期EMAを下から上に抜けてクロスした直後に現在の終値が閾値より下にある場合、次のバーで新規成行買
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx == 0:
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        low = self.ohlcv.values['low'][idx]
        fast_ema_before = self.fast_ema.ema[idx - 1]
        fast_ema_current = self.fast_ema.ema[idx]
        slow_ema_before = self.slow_ema.ema[idx - 1]
        slow_ema_current = self.slow_ema.ema[idx]
        above_cross_flg = fast_ema_before < slow_ema_before and fast_ema_current > slow_ema_current
        threshold_flg = close < low + self.price_threshold
        if above_cross_flg and threshold_flg:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        短期EMAが長期EMAを上から下に抜けてクロスした直後に現在の終値が閾値より上にある場合、次のバーで新規成行売
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx == 0:
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        high = self.ohlcv.values['high'][idx]
        fast_ema_before = self.fast_ema.ema[idx - 1]
        fast_ema_current = self.fast_ema.ema[idx]
        slow_ema_before = self.slow_ema.ema[idx - 1]
        slow_ema_current = self.slow_ema.ema[idx]
        below_cross_flg = fast_ema_before > slow_ema_before and fast_ema_current < slow_ema_current
        threshold_flg = close > high - self.price_threshold
        if below_cross_flg and threshold_flg:
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
        ind1 = self.fast_ema.ema[idx]
        ind2 = self.slow_ema.ema[idx]
        ind3 = None
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class ATRBasedBreakout(EntryStrategy):
    """
    Long:終値+(ATR*XX)に逆指値注文する
    Short:終値-(ATR*XX)に逆指値注文する
    """

    def __init__(self, title, ohlcv, long_atr, long_atr_ratio, short_atr, short_atr_ratio, vol_ema,
                 order_vol_ratio=0.01):
        self.title = title
        self.ohlcv = ohlcv
        self.long_atr = long_atr
        self.long_atr_ratio = long_atr_ratio
        self.short_atr = short_atr
        self.short_atr_ratio = short_atr_ratio
        self.vol_ema = vol_ema
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.long_atr.upper_atrband[idx] == 0
                or self.long_atr.lower_atrband[idx] == 0
                or self.long_atr.ema[idx] == 0
                or self.short_atr.upper_atrband[idx] == 0
                or self.short_atr.lower_atrband[idx] == 0
                or self.short_atr.ema[idx] == 0
                or self.vol_ema.vol_ema[idx] == 0):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        # 当日高値がバンド以上
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if self.long_atr_ratio == 0:
            return OrderType.NONE_ORDER
        else:
            return OrderType.OCO
            # return OrderType.STOP_MARKET_LONG
            # return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        # 当日安値がバンド以下
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if self.short_atr_ratio == 0:
            return OrderType.NONE_ORDER
        else:
            return OrderType.OCO
            # return OrderType.STOP_MARKET_SHORT
            # return OrderType.NONE_ORDER

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
        close = self.ohlcv.values['close'][idx]
        atrband = self.long_atr.atr[idx] * self.long_atr_ratio
        price = close + atrband
        return price

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        close = self.ohlcv.values['close'][idx]
        atrband = self.short_atr.atr[idx] * self.short_atr_ratio
        price = close - atrband
        return price

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
        ind1 = self.long_atr.ema[idx]
        ind2 = self.long_atr.atr[idx]
        ind3 = self.long_atr.atr[idx] * self.long_atr_ratio
        ind4 = self.short_atr.ema[idx]
        ind5 = self.short_atr.atr[idx]
        ind6 = self.short_atr.atr[idx] * self.short_atr_ratio
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

    def get_vol_indicators(self, idx, last_exit_idx):
        ind1 = self.vol_ema.vol_ema[idx]
        ind2 = None
        ind3 = None
        ind4 = None
        ind5 = None
        return ind1, ind2, ind3, ind4, ind5

from lii3ra.ordertype import OrderType
from lii3ra.tick import Tick
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class BreakoutATR(EntryStrategy):
    """高値または安値がATRBANDを超えた場合に逆指値注文する"""

    def __init__(self, title, ohlcv, long_atr, short_atr, vol_ema, order_vol_ratio=0.01):
        self.title = title
        self.ohlcv = ohlcv
        self.long_atr = long_atr
        self.short_atr = short_atr
        self.vol_ema = vol_ema
        self.symbol = self.ohlcv.symbol
        self.tick = Tick.get_tick(self.symbol)
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.long_atr.upper_atrband[idx] == 0
                or self.long_atr.lower_atrband[idx] == 0
                or self.long_atr.ema[idx] == 0
                or self.short_atr.upper_atrband[idx] == 0
                or self.short_atr.lower_atrband[idx] == 0
                or self.short_atr.ema[idx] == 0):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        # 当日高値がバンド以上
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        long_flg = self.ohlcv.values['high'][idx] >= self.long_atr.upper_atrband[idx]
        short_flg = self.ohlcv.values['low'][idx] <= self.long_atr.lower_atrband[idx]
        if long_flg == True and short_flg == False:
            return OrderType.STOP_MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        # 当日安値がバンド以下
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        long_flg = self.ohlcv.values['high'][idx] >= self.short_atr.upper_atrband[idx]
        short_flg = self.ohlcv.values['low'][idx] <= self.short_atr.lower_atrband[idx]
        if long_flg == False and short_flg == True:
            return OrderType.STOP_MARKET_SHORT
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
        price = self.ohlcv.values['high'][idx] + self.tick
        return price

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        price = self.ohlcv.values['low'][idx] - self.tick
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
        ind2 = self.long_atr.upper_atrband[idx]
        ind3 = self.long_atr.lower_atrband[idx]
        ind4 = self.short_atr.ema[idx]
        ind5 = self.short_atr.upper_atrband[idx]
        ind6 = self.short_atr.lower_atrband[idx]
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

    def get_vol_indicators(self, idx, last_exit_idx):
        ind1 = self.vol_ema.vol_ema[idx]
        ind2 = None
        ind3 = None
        ind4 = None
        ind5 = None
        return ind1, ind2, ind3, ind4, ind5

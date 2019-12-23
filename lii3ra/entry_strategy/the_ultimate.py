import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class TheUltimate(EntryStrategy):
    """
    THE ULTIMATE
    """
    def __init__(self
                 , title
                 , ohlcv
                 , lookback
                 , uo
                 , order_vol_ratio=0.01):
        self.title = title
        self.ohlcv = ohlcv
        self.symbol = self.ohlcv.symbol
        self.lookback = lookback
        self.uo = uo
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.uo.uo[idx] == 0
                or np.isnan(self.uo.uo[idx])
                or self.uo.uo[idx] is None
        ):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        """
Var: xbars(10);
if UltimateOsc(7,14,28)= lowest(UltimateOsc(7,14,28),xbars) then buy next bar at market;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.uo.avg3:
            return OrderType.NONE_ORDER
        uo_value = self.uo.uo[idx]
        lowest_uo_value = self.uo.uo[idx-self.lookback:idx+1].min()
        if uo_value == lowest_uo_value:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
Var: xbars(10);
if UltimateOsc(7,14,28)= highest(UltimateOsc(7,14,28),xbars) then sellshort next bar at market;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.uo.avg3:
            return OrderType.NONE_ORDER
        uo_value = self.uo.uo[idx]
        highest_uo_value = self.uo.uo[idx-self.lookback:idx+1].max()
        if uo_value == highest_uo_value:
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
        ind1 = self.uo.uo[idx]
        ind2 = None
        ind3 = None
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

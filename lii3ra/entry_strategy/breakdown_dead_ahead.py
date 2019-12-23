
from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class BreakdownDeadAhead(EntryStrategy):
    """
    高値または安値がATRBANDを超えた場合に逆指値注文する
    """
    def __init__(self
                 , title
                 , ohlcv
                 , atr
                 , length_of_trend
                 , atr_mult
                 , order_vol_ratio=0.01):
        self.title = title
        self.ohlcv = ohlcv
        self.atr = atr
        self.length_of_trend = length_of_trend
        self.atr_mult = atr_mult
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if self.atr.atr[idx] == 0:
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        """
Var: momen(10); //length of trend
Var: mult(2); //multiplier for the average true range
var:myrange(0);
myrange=truerange; //true range is a Tradestation reserved word
If close<close[momen] then buy next bar at close+mult*average(myRange,3) stop;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.length_of_trend:
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        closex = self.ohlcv.values['close'][idx-self.length_of_trend]
        long_condition = close < closex
        if long_condition:
            return OrderType.STOP_MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
Var: momen(10); //length of trend
Var: mult(2); //multiplier for the average true range
var:myrange(0);
myrange=truerange; //true range is a Tradestation reserved word
If close>close[momen] then sellshort next bar at closemult* average(myRange,3) stop;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.length_of_trend:
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        closex = self.ohlcv.values['close'][idx-self.length_of_trend]
        short_condition = close > closex
        if short_condition:
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
        price = self.ohlcv.values['close'][idx] + self.atr.atr[idx] * self.atr_mult
        return price

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        price = self.ohlcv.values['close'][idx] - self.atr.atr[idx] * self.atr_mult
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
        ind1 = self.atr.atr[idx]
        ind2 = self.ohlcv.values['close'][idx] + self.atr.atr[idx] * self.atr_mult
        ind3 = self.ohlcv.values['close'][idx] - self.atr.atr[idx] * self.atr_mult
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7


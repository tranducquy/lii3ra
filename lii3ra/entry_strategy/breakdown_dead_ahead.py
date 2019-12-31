import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.average_true_range import AverageTrueRange
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class BreakdownDeadAheadFactory(EntryStrategyFactory):
    params = {
        # atr_span, length_of_trend, atr_mult
        "default": [3, 10, 2.0]
    }

    rough_params = [
        [3, 10, 2.0]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            atr_span = self.params[s][0]
            length_of_trend = self.params[s][1]
            atr_mult = self.params[s][2]
        else:
            atr_span = self.params["default"][0]
            length_of_trend = self.params["default"][1]
            atr_mult = self.params["default"][2]
        return BreakdownDeadAhead(ohlcv, atr_span, length_of_trend, atr_mult)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            for p in self.rough_params:
                strategies.append(BreakdownDeadAhead(ohlcv
                                                     , p[0]
                                                     , p[1]
                                                     , p[2]))
        else:
            atr_span_ary = [i for i in range(1, 5, 1)]
            length_of_trend_ary = [i for i in range(5, 20, 3)]
            atr_mult_ary = [i for i in np.arange(0.5, 3.0, 0.5)]
            for atr_span in atr_span_ary:
                for length_of_trend in length_of_trend_ary:
                    for atr_mult in atr_mult_ary:
                        strategies.append(BreakdownDeadAhead(ohlcv, atr_span, length_of_trend, atr_mult))
        return strategies


class BreakdownDeadAhead(EntryStrategy):
    """
    モメンタムにあわせて逆指値注文する
    """

    def __init__(self
                 , ohlcv
                 , atr_span
                 , length_of_trend
                 , atr_mult
                 , order_vol_ratio=0.01):
        self.title = f"BreakdownDeadAhead[{atr_span:.0f},{length_of_trend:.0f}][{atr_mult:.2f}]"
        self.ohlcv = ohlcv
        self.atr = AverageTrueRange(ohlcv, atr_span)
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
        closex = self.ohlcv.values['close'][idx - self.length_of_trend]
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
        closex = self.ohlcv.values['close'][idx - self.length_of_trend]
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

import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class WhereYouAtFactory(EntryStrategyFactory):
    params = {
        # long_bb_span, long_bb_ratio, short_bb_span, short_bb_ratio
        "default": [0.50, 0.50]
    }

    rough_params = [
        [0.50, 0.50]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            long_threshold = self.params[s][0]
            short_threshold = self.params[s][1]
        else:
            long_threshold = self.params["default"][0]
            short_threshold = self.params["default"][1]
        return WhereYouAt(ohlcv, long_threshold, short_threshold)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            for p in self.rough_params:
                strategies.append(WhereYouAt(ohlcv
                                             , p[0]
                                             , p[1]))
        else:
            long_values = [i for i in np.arange(0.1, 1.0, 0.2)]
            short_values = [i for i in np.arange(0.1, 1.0, 0.2)]
            for long_value in long_values:
                for short_value in short_values:
                    strategies.append(WhereYouAt(ohlcv, long_value, short_value))
        return strategies


class WhereYouAt(EntryStrategy):
    """
    WHERE YOU AT
    """

    def __init__(self
                 , ohlcv
                 , long_threshold
                 , short_threshold
                 , order_vol_ratio=0.01):
        self.title = f"WhereYouAt[{long_threshold:.2f}][{short_threshold:.2f}]"
        self.ohlcv = ohlcv
        self.long_threshold = long_threshold
        self.short_threshold = short_threshold
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def check_entry_long(self, idx, last_exit_idx):
        """
#Var: ll(0), hh(0);
#Var: Thresh(.5); // threshold value for entries, between 0 and 1
#if time<1600 or time>2300 then begin
#   ll=minlist(l,l[1]);
#   hh=maxlist(h,h[1]);
#   if (c-ll)/(hh-ll+.000001)<=(1-thresh) then buy next bar at market;
#end;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx < 2:
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        min_low = self.ohlcv.values['low'][idx:idx + 1].min()
        max_high = self.ohlcv.values['high'][idx:idx + 1].max()
        if (close - min_low) / (max_high - min_low + 0.000001) <= (1 - self.long_threshold):
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
#Var: ll(0), hh(0);
#Var: Thresh(.5); // threshold value for entries, between 0 and 1
#if time<1600 or time>2300 then begin
#   ll=minlist(l,l[1]);
#   hh=maxlist(h,h[1]);
#   if (c-ll)/(hh-ll+.000001)>=thresh then sellshort next bar at market;
#end;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx < 2:
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        min_low = self.ohlcv.values['low'][idx:idx + 1].min()
        max_high = self.ohlcv.values['high'][idx:idx + 1].max()
        if (close - min_low) / (max_high - min_low + 0.000001) >= self.short_threshold:
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

from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class WhereYouAt(EntryStrategy):
    """

    """
    def __init__(self
                , title
                , ohlcv
                , long_threshold
                , short_threshold
                , order_vol_ratio=0.01):
        self.title                 = title
        self.ohlcv                 = ohlcv
        self.long_threshold        = long_threshold
        self.short_threshold       = short_threshold
        self.symbol                = self.ohlcv.symbol
        self.order_vol_ratio       = order_vol_ratio
    
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
        min_low = self.ohlcv.values['low'][idx:idx+1].min()
        max_high = self.ohlcv.values['high'][idx:idx+1].max()
        if (close-min_low)/(max_high-min_low+0.000001)<=(1-self.long_threshold):
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
        min_low = self.ohlcv.values['low'][idx:idx+1].min()
        max_high = self.ohlcv.values['high'][idx:idx+1].max()
        if (close-min_low)/(max_high-min_low+0.000001)>=self.short_threshold:
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

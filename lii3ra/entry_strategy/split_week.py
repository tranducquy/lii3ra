from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class SplitWeek(EntryStrategy):
    """
Var: bbars(15); // lookbar period for the recent highest and lowest prices
Var: maxl(2500); // max allowable average true range, converted to dollars per contract
Condition1 = dayofweek(date)=2 dayofweek(date)=4; //True or False
If Condition1 and high=highest(high,bbars) and close=highest(close,bbars) and avgtruerange(14)*BigPointValue<maxl then buy next bar at market;
If Condition1 and low=lowest(low,bbars) and close=lowest(close,bbars) and avgtruerange(14)*BigPointValue<maxl then sellshort next bar at market;
    """
    def __init__(self
                 , title
                 , ohlcv
                 , atr
                 , atr_ratio
                 , lookback
                 , maxl
                 , entry_dayofweek
                 , order_vol_ratio=0.01
                 ):
        self.title = title
        self.ohlcv = ohlcv
        self.atr = atr
        self.atr_ratio = atr_ratio
        self.lookback = lookback
        self.maxl = maxl
        self.entry_dayofweek = entry_dayofweek
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio
    
    def _is_indicator_valid(self, idx):
        if (
               self.atr.atr[idx] == 0
        ):
            return False
        else:
            return True

    def _is_d(self):
        if self.ohlcv.ashi == "1d":
            return True
        else:
            return False

    def check_entry_long(self, idx, last_exit_idx):
        """
Condition1 = dayofweek(date)=2 dayofweek(date)=4; //True or False
If Condition1 and high=highest(high,bbars) and close=highest(close,bbars) and avgtruerange(14)*BigPointValue<maxl then buy next bar at market;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_d:
            return OrderType.NONE_ORDER
        current_weekday = self.ohlcv.values['time'][idx].weekday()
        highest_high = self.ohlcv.values['high'][idx-self.lookback:idx+1].max()
        highest_close = self.ohlcv.values['close'][idx-self.lookback:idx+1].max()
        high = self.ohlcv.values['high'][idx]
        close = self.ohlcv.values['close'][idx]
        condition1 = current_weekday in self.entry_dayofweek
        condition2 = highest_high == high and highest_close == close
        condition3 = self.atr.atr[idx] * self.atr_ratio < self.maxl
        if condition1 and condition2 and condition3:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
Condition1 = dayofweek(date)=2 dayofweek(date)=4; //True or False
If Condition1 and low=lowest(low,bbars) and close=lowest(close,bbars) and avgtruerange(14)*BigPointValue<maxl then sellshort next bar at market;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_d:
            return OrderType.NONE_ORDER
        current_weekday = self.ohlcv.values['time'][idx].weekday()
        lowest_low = self.ohlcv.values['low'][idx-self.lookback:idx+1].min()
        lowest_close = self.ohlcv.values['close'][idx-self.lookback:idx+1].min()
        low = self.ohlcv.values['low'][idx]
        close = self.ohlcv.values['close'][idx]
        condition1 = current_weekday in self.entry_dayofweek
        condition2 = lowest_low == low and lowest_close == close
        condition3 = self.atr.atr[idx] * self.atr_ratio < self.maxl
        if condition1 and condition2 and condition3:
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
        close = self.ohlcv.values['close'][idx]
        atrband = self.atr.atr[idx] * self.atr_ratio
        price = close + atrband
        return price

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        close = self.ohlcv.values['close'][idx]
        atrband = self.atr.atr[idx] * self.atr_ratio
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
        ind1 = self.maxl
        ind2 = self.atr.atr[idx]
        ind3 = self.atr.atr[idx] * self.atr_ratio
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7


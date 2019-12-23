import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.tick import Tick
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class IntradayBreakoutWithExpandingRange(EntryStrategy):
    """
    INTRADAY BREAKOUT WITH EXPANDING RANGE
Var: tbeg(945); // signal window start time
Var: tend(1045); //signal window end time
Var: offset(.1); //additional amount the price has to break the high or low before entering a trade – can be zero if desired
Var: adxP(10); // ADX lookback period
Var: adxThresh(20); // ADX threshold for signifying a trend
if time>=tbeg and time<=tend then begin
    if EntriesToday(date[0])<1 and adx (adxP) >= AdxThresh and (highd(1)-lowd(1) > highd(2)-lowd(2)) then begin
        buy next bar at highd(1) + Offset Points stop;
        sellshort next bar at lowd(1) - Offset points stop;
    end;
end;
    """

    def __init__(self
                 , title
                 , ohlcv
                 , adx
                 , adx_threshold
                 , begin_time
                 , end_time
                 , order_vol_ratio=0.01):
        self.title = title
        self.ohlcv = ohlcv
        self.adx = adx
        self.adx_threshold = adx_threshold
        self.begin_time = begin_time
        self.end_time = end_time
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio
        self.tick = Tick.get_tick(self.symbol)
        self.firstday = None
        self.stop_long_value = None
        self.stop_short_value = None
        self.trade_days = None

    def is_intraday(self, idx):
        current_time = self.ohlcv.values['time'][idx].strftime("%H%M%S")
        if self.begin_time <= current_time <= self.end_time:
            return True
        else:
            return False

    def is_firstday(self, idx):
        current_day = self.ohlcv.values['time'][idx].strftime("%Y%m%d")
        if self.firstday is None:
            self.firstday = current_day
            return True
        elif self.firstday == current_day:
            return True
        else:
            return False

    def check_entry_long(self, idx, last_exit_idx):
        """
    if EntriesToday(date[0])<1 and adx (adxP) >= AdxThresh and (highd(1)-lowd(1) > highd(2)-lowd(2)) then begin
        buy next bar at highd(1) + Offset Points stop;
    end;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if self.is_firstday(idx):
            return OrderType.NONE_ORDER
        if not self.is_intraday(idx):
            return OrderType.NONE_ORDER
        highest_high1, highest_high2 = self._get_highest_highs(idx)
        lowest_low1, lowest_low2 = self._get_lowest_lows(idx)
        condition1 = self.adx.adx[idx] >= self.adx_threshold
        condition2 = highest_high1 - lowest_low1 > highest_high2 - lowest_low2
        if condition1 and condition2:
            return OrderType.OCO
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
    if EntriesToday(date[0])<1 and adx (adxP) >= AdxThresh and (highd(1)-lowd(1) > highd(2)-lowd(2)) then begin
        sellshort next bar at lowd(1) - Offset points stop;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if self.is_firstday(idx):
            return OrderType.NONE_ORDER
        if not self.is_intraday(idx):
            return OrderType.NONE_ORDER
        highest_high1, highest_high2 = self._get_highest_highs(idx)
        lowest_low1, lowest_low2 = self._get_lowest_lows(idx)
        condition1 = self.adx.adx[idx] >= self.adx_threshold
        condition2 = highest_high1 - lowest_low1 > highest_high2 - lowest_low2
        if condition1 and condition2:
            return OrderType.OCO
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
        highest_high1, _ = self._get_highest_highs(idx)
        if np.isnan(highest_high1) or highest_high1 == 0:
            return -1
        self.stop_long_value = highest_high1 + self.tick
        return self.stop_long_value

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        lowest_low1, _ = self._get_lowest_lows(idx)
        if np.isnan(lowest_low1) or lowest_low1 == 0:
            return -1
        self.stop_short_value = lowest_low1 - self.tick
        return self.stop_short_value

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
        ind1 = self.adx.adx[idx]
        ind2 = self.stop_long_value
        ind3 = self.stop_short_value
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

    def _get_before_day(self, current_day):
        if self.trade_days is None:
            self.trade_days = self.ohlcv.values['time'].dt.date
        past_trade_days = self.trade_days[self.trade_days < current_day]
        before_day = past_trade_days.max()
        return before_day

    def _get_highest_highs(self, idx):
        current_day = self.ohlcv.values['time'][idx].date()
        before_day1 = self._get_before_day(current_day)
        before_day2 = self._get_before_day(before_day1)
        past_highs1 = self.ohlcv.values['high'][self.ohlcv.values['time'].dt.date == before_day1]
        past_highs2 = self.ohlcv.values['high'][self.ohlcv.values['time'].dt.date == before_day2]
        highest_high1 = past_highs1.max()
        highest_high2 = past_highs2.max()
        return highest_high1, highest_high2

    def _get_lowest_lows(self, idx):
        current_day = self.ohlcv.values['time'][idx].date()
        before_day1 = self._get_before_day(current_day)
        before_day2 = self._get_before_day(before_day1)
        past_lows1 = self.ohlcv.values['low'][self.ohlcv.values['time'].dt.date == before_day1]
        past_lows2 = self.ohlcv.values['low'][self.ohlcv.values['time'].dt.date == before_day2]
        lowest_low1 = past_lows1.min()
        lowest_low2 = past_lows2.min()
        return lowest_low1, lowest_low2



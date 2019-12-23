import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.tick import Tick
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class IntradayBreakout(EntryStrategy):
    """
    INTRADAY BREAKOUT
Var: tbeg(945); // signal window start time
Var: tend(1045); //signal window end time
Var: offset(.1); //additional amount the price has to break the high or low before entering a trade – can be zero if desired
Var: adxP(10); // ADX lookback period
Var: adxThresh(20); // ADX threshold for signifying a trend
if time>=tbeg and time<=tend then begin
    if EntriesToday(date[0])<1 and adx (adxP) >= AdxThresh then begin
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
        if self.firstday == current_day:
            return True
        else:
            return False

    def check_entry_long(self, idx, last_exit_idx):
        """
    if EntriesToday(date[0])<1 and adx (adxP) >= AdxThresh then begin
        buy next bar at highd(1) + Offset Points stop;
    end;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self.is_intraday(idx):
            return OrderType.NONE_ORDER
        if self.is_firstday(idx):
            return OrderType.NONE_ORDER
        condition1 = self.adx.adx[idx] >= self.adx_threshold
        if condition1:
            return OrderType.OCO
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
    if EntriesToday(date[0])<1 and adx (adxP) >= AdxThresh then begin
        sellshort next bar at lowd(1) - Offset points stop;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self.is_intraday(idx):
            return OrderType.NONE_ORDER
        if self.is_firstday(idx):
            return OrderType.NONE_ORDER
        condition1 = self.adx.adx[idx] >= self.adx_threshold
        if condition1:
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
        trade_days = self.ohlcv.values['time'].dt.date
        current_day = self.ohlcv.values['time'][idx].date()
        past_trade_days = trade_days[trade_days < current_day]
        before_day = past_trade_days.max()
        past_highs = self.ohlcv.values['high'][self.ohlcv.values['time'].dt.date == before_day]
        highest_high = past_highs.max()
        if np.isnan(highest_high) or highest_high == 0:
            return -1
        return highest_high + self.tick

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        trade_days = self.ohlcv.values['time'].dt.date
        current_day = self.ohlcv.values['time'][idx].date()
        past_trade_days = trade_days[trade_days < current_day]
        before_day = past_trade_days.max()
        past_lows = self.ohlcv.values['low'][self.ohlcv.values['time'].dt.date == before_day]
        lowest_low = past_lows.min()
        if np.isnan(lowest_low) or lowest_low == 0:
            return -1
        return lowest_low - self.tick

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
        ind2 = None
        ind3 = None
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

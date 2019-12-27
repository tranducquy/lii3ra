import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy
from lii3ra.tick import Tick


class EconomicCalenderFactory(EntryStrategyFactory):
    params = {
        # long_dayofweek, long_time, short_dayofweek, short_time
        "default": [[2], "093000", [3], "093000"]
    }

    rough_params = [
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            long_dayofweek = self.params[s][0]
            long_time = self.params[s][1]
            short_dayofweek = self.params[s][2]
            short_time = self.params[s][3]
        else:
            long_dayofweek = self.params["default"][0]
            long_time = self.params["default"][1]
            short_dayofweek = self.params["default"][2]
            short_time = self.params["default"][3]
        return EconomicCalender(ohlcv, long_dayofweek, long_time, short_dayofweek, short_time)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        long_dayofweek_list = [i for i in range(7)]
        long_time_list = [f"{i:02.0f}0000" for i in range(25)]
        short_dayofweek_list = [i for i in range(7)]
        short_time_list = [f"{i:02.0f}0000" for i in range(25)]
        for long_dayofweek in long_dayofweek_list:
            for long_time in long_time_list:
                strategies.append(EconomicCalender(ohlcv
                                                   , long_dayofweek
                                                   , long_time
                                                   , self.params["default"][2]
                                                   , self.params["default"][3]))
        for short_dayofweek in short_dayofweek_list:
            for short_time in short_time_list:
                strategies.append(EconomicCalender(ohlcv
                                                   , self.params["default"][0]
                                                   , self.params["default"][1]
                                                   , short_dayofweek
                                                   , short_time))
        return strategies


class EconomicCalender(EntryStrategy):
    """
    ECONOMIC CALENDER
    * 分足のみ
If time=935 and dayofweek(date)= 3 then Buy next bar at highd(1) stop;
If time=935 and dayofweek(date)= 4 then SellShort next bar at lowd(1) stop;
    """
    def __init__(self
                 , ohlcv
                 , long_dayofweek
                 , long_time
                 , short_dayofweek
                 , short_time
                 , order_vol_ratio=0.01):
        long_entry_dayofweek_title = ",".join(map(str, long_dayofweek))
        short_entry_dayofweek_title = ",".join(map(str, short_dayofweek))
        self.title = f"EconomicCalender[{long_entry_dayofweek_title},{long_time}]"\
                     f"[{short_entry_dayofweek_title},{short_time}]"
        self.ohlcv = ohlcv
        self.long_dayofweek = long_dayofweek
        self.long_time = long_time
        self.short_dayofweek = short_dayofweek
        self.short_time = short_time
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio
        self.firstday = None
        self.stop_long_value = None
        self.stop_short_value = None
        self.tick = Tick.get_tick(self.symbol)
        self.trade_days = None

    def is_firstday(self, idx):
        current_day = self.ohlcv.values['time'][idx].strftime("%Y%m%d")
        if self.firstday is None:
            self.firstday = current_day
            return True
        if self.firstday == current_day:
            return True
        else:
            return False

    def is_entrytime(self, idx, entrytime):
        current_time = self.ohlcv.values['time'][idx].strftime("%H%M%S")
        if entrytime == current_time:
            return True
        else:
            return False

    def check_entry_long(self, idx, last_exit_idx):
        """
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self.is_entrytime(idx, self.long_time):
            return OrderType.NONE_ORDER
        dayofweek = self.ohlcv.values['time'][idx].weekday()
        if dayofweek in self.long_dayofweek:
            return OrderType.STOP_MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self.is_entrytime(idx, self.short_time):
            return OrderType.NONE_ORDER
        dayofweek = self.ohlcv.values['time'][idx].weekday()
        if dayofweek in self.short_dayofweek:
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
        highest_high1 = self._get_highest_high(idx)
        if np.isnan(highest_high1) or highest_high1 == 0:
            return -1
        self.stop_long_value = highest_high1 + self.tick
        return self.stop_long_value

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        lowest_low1 = self._get_lowest_low(idx)
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
        ind1 = None
        ind2 = None
        ind3 = None
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

    def _get_highest_high(self, idx):
        current_day = self.ohlcv.values['time'][idx].date()
        before_day1 = self._get_before_day(current_day)
        past_highs1 = self.ohlcv.values['high'][self.ohlcv.values['time'].dt.date == before_day1]
        highest_high1 = past_highs1.max()
        return highest_high1

    def _get_lowest_low(self, idx):
        current_day = self.ohlcv.values['time'][idx].date()
        before_day1 = self._get_before_day(current_day)
        past_lows1 = self.ohlcv.values['low'][self.ohlcv.values['time'].dt.date == before_day1]
        lowest_low1 = past_lows1.min()
        return lowest_low1


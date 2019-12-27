from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class ItsAboutTimeFactory(EntryStrategyFactory):
    params = {
        # lookback, long_time, short_time
        "default": [12, "100000", "110000"]
    }

    rough_params = [
        [12, "100000", "100000"]
        , [12, "110000", "110000"]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            lookback = self.params[s][0]
            long_time = self.params[s][1]
            short_time = self.params[s][2]
        else:
            lookback = self.params["default"][0]
            long_time = self.params["default"][1]
            short_time = self.params["default"][2]
        return ItsAboutTime(ohlcv, lookback, long_time, short_time)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            # strategies = self._optimization_rough(ohlcv)
            for p in self.rough_params:
                strategies.append(ItsAboutTime(ohlcv, p[0], p[1], p[2]))
        else:
            lookback_list = [i for i in range(4, 15, 2)]
            long_time_list = [f"{i:02.0f}0000" for i in range(25)]
            short_time_list = [f"{i:02.0f}0000" for i in range(25)]
            for lookback in lookback_list:
                for long_time in long_time_list:
                    strategies.append(ItsAboutTime(ohlcv, lookback, long_time, self.params["default"][2]))
            for lookback in lookback_list:
                for short_time in short_time_list:
                    strategies.append(ItsAboutTime(ohlcv, lookback, self.params["default"][1], short_time))
        return strategies


class ItsAboutTime(EntryStrategy):
    """
    IT'S ABOUT TIME
     * 分足のみ
    """

    def __init__(self
                 , ohlcv
                 , lookback
                 , long_time
                 , short_time
                 , order_vol_ratio=0.01):
        self.title = f"ItsAboutTime[{lookback:.0f},{long_time},{short_time}]"
        self.ohlcv = ohlcv
        self.lookback = lookback
        self.long_time = long_time
        self.short_time = short_time
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def check_entry_long(self, idx, last_exit_idx):
        """
Var:barsback (10);
Var:BullSignalTime(False), BearSignalTime(false);
If (time>300 and time[1]<=300) or (time>2130 and time[1]<=2130) then Bullsignaltime=True;
If (time>900 and time[1]<=900) then Bearsignaltime=True;
if Bullsignaltime and close>close[barsback] then Buy next bar at close limit;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.lookback:
            return OrderType.NONE_ORDER
        current_time = self.ohlcv.values['time'][idx].strftime("%H%M%S")
        before_time = self.ohlcv.values['time'][idx - 1].strftime("%H%M%S")
        close = self.ohlcv.values['close'][idx]
        close_lookback = self.ohlcv.values['close'][idx - self.lookback]
        long_flg1 = current_time > self.long_time >= before_time
        long_flg2 = close > close_lookback
        if long_flg1 and long_flg2:
            return OrderType.LIMIT_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
Var:barsback (10);
Var:BullSignalTime(False), BearSignalTime(false);
If (time>300 and time[1]<=300) or (time>2130 and time[1]<=2130) then Bullsignaltime=True;
If (time>900 and time[1]<=900) then Bearsignaltime=True;
if Bearsignaltime and close<close[barsback] then sellshort next bar at close limit;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.lookback:
            return OrderType.NONE_ORDER
        current_time = (self.ohlcv.values['time'][idx]).strftime("%H%M%S")
        before_time = self.ohlcv.values['time'][idx - 1].strftime("%H%M%S")
        close = self.ohlcv.values['close'][idx]
        close_lookback = self.ohlcv.values['close'][idx - self.lookback]
        short_flg1 = current_time > self.short_time >= before_time
        short_flg2 = close < close_lookback
        if short_flg1 and short_flg2:
            return OrderType.LIMIT_SHORT
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

    def create_order_open_long_limit_for_all_cash(self, cash, idx, last_exit_idx):
        if not self._is_valid(idx) or cash <= 0:
            return -1, -1
        price = self.create_order_open_long_limit(idx, last_exit_idx)
        vol = self.get_order_vol(cash, idx, price, last_exit_idx)
        return price, vol

    def create_order_open_short_limit_for_all_cash(self, cash, idx, last_exit_idx):
        if not self._is_valid(idx) or cash <= 0:
            return -1, -1
        price = self.create_order_open_short_limit(idx, last_exit_idx)
        vol = self.get_order_vol(cash, idx, price, last_exit_idx)
        return price, vol * -1

    def create_order_open_long_limit(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        price = self.ohlcv.values['close'][idx]
        return price

    def create_order_open_short_limit(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        price = self.ohlcv.values['close'][idx]
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
        ind1 = None
        ind2 = None
        ind3 = None
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

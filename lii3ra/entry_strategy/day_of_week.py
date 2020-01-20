from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class DayOfWeekFactory(EntryStrategyFactory):
    params = {
        # long_dayofweek, short_dayofweek
        "default": [3, 4]
    }

    def create(self, ohlcv, optimization=False):
        strategies = []
        if not optimization:
            s = ohlcv.symbol
            if s in self.params:
                long_dayofweek = self.params[s][0]
                short_dayofweek = self.params[s][1]
            else:
                long_dayofweek = self.params["default"][0]
                short_dayofweek = self.params["default"][1]
            strategies.append(DayOfWeek(ohlcv, long_dayofweek, short_dayofweek))
        else:
            long_dayofweek_list = [i for i in range(7)]
            short_dayofweek_list = [i for i in range(7)]
            for long_dayofweek in long_dayofweek_list:
                strategies.append(DayOfWeek(ohlcv, long_dayofweek, self.params["default"][1]))
            for short_dayofweek in short_dayofweek_list:
                strategies.append(DayOfWeek(ohlcv, self.params["default"][0], short_dayofweek))
        return strategies


class DayOfWeek(EntryStrategy):
    """
    DAY OF WEEK
     * 日足のみ
    """

    def __init__(self
                 , ohlcv
                 , long_dayofweek
                 , short_dayofweek
                 , order_vol_ratio=0.01):
        self.title = f"DayOfWeek[{long_dayofweek:.0f},{short_dayofweek:.0f}]"
        self.ohlcv = ohlcv
        self.long_dayofweek = long_dayofweek
        self.short_dayofweek = short_dayofweek
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def is_d(self):
        if self.ohlcv.ashi == "1d":
            return True
        else:
            return False

    def check_entry_long(self, idx, last_exit_idx):
        """
        金曜日はロング
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self.is_d():
            return OrderType.NONE_ORDER
        dayofweek = self.ohlcv.values['time'][idx].weekday()
        if dayofweek == self.long_dayofweek:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        月曜日はショート
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self.is_d():
            return OrderType.NONE_ORDER
        dayofweek = self.ohlcv.values['time'][idx].weekday()
        if dayofweek == self.short_dayofweek:
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



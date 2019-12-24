from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class EveryoneLovesFridayFactory(EntryStrategyFactory):
    params = {
        # lookback_span, long_weekday, short_weekday
        "default": [25, [4], [4]]
        # , "^N225": [3, 1.0, 3, 1.0]
    }

    rough_params = [
        [25, [4], [4]]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            lookback_span = self.params[s][0]
            long_weekday = self.params[s][1]
            short_weekday = self.params[s][2]
        else:
            lookback_span = self.params["default"][0]
            long_weekday = self.params["default"][1]
            short_weekday = self.params["default"][2]
        return EveryoneLovesFriday(ohlcv
                                   , lookback_span
                                   , long_weekday
                                   , short_weekday)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            for p in self.rough_params:
                strategies.append(EveryoneLovesFriday(ohlcv
                                                      , p[0]
                                                      , p[1]
                                                      , p[2]
                                                      ))
        else:
            lookback_spans = [i for i in range(5, 30, 5)]
            long_weekdays = [[0], [1], [2], [3], [4], [5], [6]]
            short_weekdays = [[0], [1], [2], [3], [4], [5], [6]]
            for lookback_span in lookback_spans:
                for long_weekday in long_weekdays:
                    strategies.append(EveryoneLovesFriday(ohlcv, lookback_span, long_weekday, []))
            for lookback_span in lookback_spans:
                for short_weekday in short_weekdays:
                    strategies.append(EveryoneLovesFriday(ohlcv, lookback_span, [], short_weekday))
        return strategies


class EveryoneLovesFriday(EntryStrategy):
    """
    EVERYONE LOVES FRIDAY
     - 日足のみ
Var:bbars(25); //number of lookback bars for the highest/lowest evaluation
if dayofweek(date)=5 and close=highest(close,bbars) then buy next bar at market;
if dayofweek(date)=5 and close=lowest(close,bbars) then sellshort next bar at market;
    """

    def __init__(self
                 , ohlcv
                 , lookback
                 , long_dayofweek
                 , short_dayofweek
                 , order_vol_ratio=0.01):
        long_entry_dayofweek_title = ",".join(map(str, long_dayofweek))
        short_entry_dayofweek_title = ",".join(map(str, short_dayofweek))
        self.title = f"EveryoneLovesFriday[{lookback:.0f}][{long_entry_dayofweek_title}][{short_entry_dayofweek_title}]"
        self.ohlcv = ohlcv
        self.lookback = lookback
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
        ??曜日はロング
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self.is_d():
            return OrderType.NONE_ORDER
        if idx <= self.lookback:
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        highest_close = self.ohlcv.values['close'][idx - self.lookback:idx + 1].max()
        dayofweek = self.ohlcv.values['time'][idx].weekday()
        condition1 = dayofweek in self.long_dayofweek
        condition2 = close == highest_close
        if condition1 and condition2:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        ??曜日はショート
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self.is_d():
            return OrderType.NONE_ORDER
        if idx <= self.lookback:
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        lowest_close = self.ohlcv.values['close'][idx - self.lookback:idx + 1].min()
        dayofweek = self.ohlcv.values['time'][idx].weekday()
        condition1 = dayofweek in self.short_dayofweek
        condition2 = close == lowest_close
        if condition1 and condition2:
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

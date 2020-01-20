from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.average_true_range import AverageTrueRange
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class SplitWeekFactory(EntryStrategyFactory):
    params = {
        # fast_atr_span, slow_atr_span, slow_atr_ratio, lookback, weekday
        "default": [5, 14, 0.5, 15, [1, 2, 3]]
        # , "^N225": [3, 1.0, 3, 1.0]
    }

    def create(self, ohlcv, optimization=False):
        strategies = []
        if not optimization:
            #
            s = ohlcv.symbol
            if s in self.params:
                fast_atr_span = self.params[s][0]
                slow_atr_span = self.params[s][1]
                slow_atr_ratio = self.params[s][2]
                lookback = self.params[s][3]
                entry_weekday = self.params[s][4]
            else:
                fast_atr_span = self.params["default"][0]
                slow_atr_span = self.params["default"][1]
                slow_atr_ratio = self.params["default"][2]
                lookback = self.params["default"][3]
                entry_weekday = self.params["default"][4]
            strategies.append(SplitWeek(ohlcv, fast_atr_span, slow_atr_span, slow_atr_ratio, lookback, entry_weekday))
        else:
            fast_atr_spans = [i for i in range(3, 6, 1)]
            slow_atr_spans = [i for i in range(10, 16, 2)]
            slow_atr_ratios = [i for i in np.arange(0.2, 0.9, 0.2)]
            lookbacks = [i for i in range(5, 16, 5)]
            weekdays = [[0], [1], [2], [3], [4]]
            for fast_atr_span in fast_atr_spans:
                for slow_atr_span in slow_atr_spans:
                    for slow_atr_ratio in slow_atr_ratios:
                        for lookback in lookbacks:
                            for weekday in weekdays:
                                strategies.append(SplitWeek(ohlcv, fast_atr_span, slow_atr_span, slow_atr_ratio, lookback, weekday))
        return strategies


class SplitWeek(EntryStrategy):
    """
     - 分足のみ
Var: bbars(15); // lookbar period for the recent highest and lowest prices
Var: maxl(2500); // max allowable average true range, converted to dollars per contract
Condition1 = dayofweek(date)=2 dayofweek(date)=4; //True or False
If Condition1 and high=highest(high,bbars) and close=highest(close,bbars) and avgtruerange(14)*BigPointValue<maxl then buy next bar at market;
If Condition1 and low=lowest(low,bbars) and close=lowest(close,bbars) and avgtruerange(14)*BigPointValue<maxl then sellshort next bar at market;
    """
    def __init__(self
                 , ohlcv
                 , fast_atr_span
                 , slow_atr_span
                 , slow_atr_ratio
                 , lookback
                 , entry_dayofweek
                 , order_vol_ratio=0.01
                 ):
        entry_dayofweek_title = ",".join(map(str, entry_dayofweek))
        self.title = f"SplitWeek1[{fast_atr_span:.0f}]"\
                     f"[{slow_atr_span:.0f},{slow_atr_ratio:.2f}][{lookback:.0f}][{entry_dayofweek_title}]"
        self.ohlcv = ohlcv
        self.fast_atr = AverageTrueRange(ohlcv, fast_atr_span)
        self.slow_atr = AverageTrueRange(ohlcv, slow_atr_span)
        self.slow_atr_ratio = slow_atr_ratio
        self.lookback = lookback
        self.entry_dayofweek = entry_dayofweek
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio
    
    def _is_indicator_valid(self, idx):
        if (
               self.fast_atr.atr[idx] == 0
               or self.slow_atr.atr[idx] == 0
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
        condition3 = self.fast_atr.atr[idx] < self.slow_atr.atr[idx]
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
        condition3 = self.fast_atr.atr[idx] < self.slow_atr.atr[idx]
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
        atrband = self.slow_atr.atr[idx] * self.slow_atr_ratio
        price = close + atrband
        return price

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        close = self.ohlcv.values['close'][idx]
        atrband = self.slow_atr.atr[idx] * self.slow_atr_ratio
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
        ind1 = self.fast_atr.atr[idx]
        ind2 = self.slow_atr.atr[idx]
        ind3 = self.slow_atr.atr[idx] * self.slow_atr_ratio
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7


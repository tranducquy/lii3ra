import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class SecondVerseSameAsTheFirstFactory(EntryStrategyFactory):
    params = {
        # threshold, lookback
        "default": [0.5, 10]
    }

    def create(self, ohlcv, optimization=False):
        strategies = []
        if not optimization:
            s = ohlcv.symbol
            if s in self.params:
                threshold = self.params[s][0]
                lookback = self.params[s][1]
            else:
                threshold = self.params["default"][0]
                lookback = self.params["default"][1]
            strategies.append(SecondVerseSameAsTheFirst(ohlcv, threshold, lookback))
        else:
            threshold_list = [i for i in np.arange(0.3, 1.0, 0.2)]
            lookback_list = [i for i in range(5, 20, 3)]
            for threshold in threshold_list:
                for lookback in lookback_list:
                    strategies.append(SecondVerseSameAsTheFirst(ohlcv, threshold, lookback))
        return strategies


class SecondVerseSameAsTheFirst(EntryStrategy):
    """
    SECOND VERSE SAME AS THE FIRST
    """

    def __init__(self, ohlcv, threshold=0.5, lookback=10, order_vol_ratio=0.01):
        super().__init__(ohlcv, order_vol_ratio)
        self.title = f"SecondVerse[{threshold:.1f},{lookback:.0f}]"
        self.threshold = threshold
        self.lookback = lookback

    def check_entry_long(self, idx, last_exit_idx):
        """
If month(date)<=6 and close=highest(close,xbar) and ((c-l)/(h-l)) <thresh then buy next bar at market;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.lookback:
            return OrderType.NONE_ORDER
        current_ts = self.ohlcv.values['time'][idx]
        current_month = current_ts.month
        close = self.ohlcv.values['close'][idx]
        highest_close = (self.ohlcv.values['close'][idx - self.lookback:idx + 1]).max()
        high = self.ohlcv.values['high'][idx]
        low = self.ohlcv.values['low'][idx]
        condition1 = current_month <= 6
        condition2 = close == highest_close
        condition3 = (close - low) / (high - low) < self.threshold
        if condition1 and condition2 and condition3:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
If month(date)>6 and close=lowest(close,xbar) and ((c-l)/(h-l))>(1-thresh) then sellshort next bar at market;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.lookback:
            return OrderType.NONE_ORDER
        current_ts = self.ohlcv.values['time'][idx]
        current_month = current_ts.month
        close = self.ohlcv.values['close'][idx]
        lowest_close = (self.ohlcv.values['close'][idx - self.lookback:idx + 1]).min()
        high = self.ohlcv.values['high'][idx]
        low = self.ohlcv.values['low'][idx]
        condition1 = current_month > 6
        condition2 = close == lowest_close
        condition3 = (close - low) / (high - low) > (1 - self.threshold)
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

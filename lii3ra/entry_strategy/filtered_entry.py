from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class FilteredEntryFactory(EntryStrategyFactory):
    params = {
        # lookback
        "default": [25]
    }

    def create(self, ohlcv, optimization=False):
        strategies = []
        if not optimization:
            #
            s = ohlcv.symbol
            if s in self.params:
                lookback = self.params[s][0]
            else:
                lookback = self.params["default"][0]
            strategies.append(FilteredEntry(ohlcv, lookback))
        else:
            lookback_list = [i for i in range(5, 35, 5)]
            for lookback in lookback_list:
                strategies.append(FilteredEntry(ohlcv, lookback))
        return strategies


class FilteredEntry(EntryStrategy):
    """
    FILTERED ENTRY
    """

    def __init__(self
                 , ohlcv
                 , lookback
                 , order_vol_ratio=0.01):
        self.title = f"FilteredEntry[{lookback:.0f}]"
        self.ohlcv = ohlcv
        self.lookback = lookback
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def check_entry_long(self, idx, last_exit_idx):
        """
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.lookback:
            return OrderType.NONE_ORDER
        high1 = self.ohlcv.values['high'][idx-1]
        low1 = self.ohlcv.values['low'][idx-1]
        high2 = self.ohlcv.values['high'][idx-2]
        low2 = self.ohlcv.values['low'][idx-2]
        highest_close = self.ohlcv.values['close'][idx-self.lookback:idx+1].max()
        close = self.ohlcv.values['close'][idx]
        condition1 = (high1-low1) < (high2-low2)
        condition2 = highest_close == close
        if condition1 and condition2:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.lookback:
            return OrderType.NONE_ORDER
        high1 = self.ohlcv.values['high'][idx-1]
        low1 = self.ohlcv.values['low'][idx-1]
        high2 = self.ohlcv.values['high'][idx-2]
        low2 = self.ohlcv.values['low'][idx-2]
        lowest_close = self.ohlcv.values['close'][idx-self.lookback:idx+1].min()
        close = self.ohlcv.values['close'][idx]
        condition1 = (high1-low1) < (high2-low2)
        condition2 = lowest_close == close
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


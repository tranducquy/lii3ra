from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class QuickPullbackPatternFactory(EntryStrategyFactory):
    params = {
    }

    rough_params = [
    ]

    def create_strategy(self, ohlcv):
        return QuickPullbackPattern(ohlcv)

    def optimization(self, ohlcv, rough=True):
        strategies = [QuickPullbackPattern(ohlcv)]
        return strategies


class QuickPullbackPattern(EntryStrategy):
    """
    QUICK PULLBACK PATTERN
    """

    def __init__(self
                 , ohlcv
                 , order_vol_ratio=0.01):
        self.title = f"QuickPullbackPattern"
        self.ohlcv = ohlcv
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def check_entry_long(self, idx, last_exit_idx):
        """
if h[2]>h[1] and l[2]<l[1] and c>h[2] then buy next bar at market;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= 3:
            return OrderType.NONE_ORDER
        high2 = self.ohlcv.values['high'][idx - 2]
        high1 = self.ohlcv.values['high'][idx - 1]
        low2 = self.ohlcv.values['low'][idx - 2]
        low1 = self.ohlcv.values['low'][idx - 1]
        close0 = self.ohlcv.values['close'][idx]
        long_flg1 = high2 > high1
        long_flg2 = low2 > low1
        long_flg3 = close0 > high2
        if long_flg1 and long_flg2 and long_flg3:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
if l[2]<l[1] and h[2]>h[1] and c<l[2] then sell short next bar at market;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= 3:
            return OrderType.NONE_ORDER
        low2 = self.ohlcv.values['low'][idx - 2]
        low1 = self.ohlcv.values['low'][idx - 1]
        high2 = self.ohlcv.values['high'][idx - 2]
        high1 = self.ohlcv.values['high'][idx - 1]
        close0 = self.ohlcv.values['close'][idx]
        short_flg1 = low2 < low1
        short_flg2 = high2 < high1
        short_flg3 = close0 < low2
        if short_flg1 and short_flg2 and short_flg3:
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

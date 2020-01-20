from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class PitterPatterPattern2Factory(EntryStrategyFactory):
    params = {
    }

    def create(self, ohlcv, optimization=False):
        strategies = [PitterPatterPattern2(ohlcv)]
        return strategies


class PitterPatterPattern2(EntryStrategy):
    """
    PITTER PATTER PATTERN2
    ロングトレード：3バー前の安値>現在の高値および現在の高値>前の安値および前の安値> 2バー前の安値および現在の終値>前の終値
    ショートトレード：すべての「高」を「低」に、すべての「>」を「<」に変更
    """

    def __init__(self
                 , ohlcv
                 , order_vol_ratio=0.01):
        self.title = f"PitterPatterPattern2"
        self.ohlcv = ohlcv
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def check_entry_long(self, idx, last_exit_idx):
        """
If l[3]>h[0] and h[0]>l[1] and l[1]>l[2] and c[0] > c[1] then buy next bar at market;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= 3:
            return OrderType.NONE_ORDER
        low3 = self.ohlcv.values['low'][idx - 3]
        high0 = self.ohlcv.values['high'][idx]
        low1 = self.ohlcv.values['low'][idx - 1]
        low2 = self.ohlcv.values['low'][idx - 2]
        close0 = self.ohlcv.values['close'][idx]
        close1 = self.ohlcv.values['close'][idx - 1]
        long_flg1 = low3 > high0
        long_flg2 = high0 > low1
        long_flg3 = low1 > low2
        long_flg4 = close0 > close1
        if long_flg1 and long_flg2 and long_flg3 and long_flg4:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
If h[3]<l[0] and l[0]<h[1] and h[1]<h[2] and c[0] < c[1] then sell short next bar at market;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= 3:
            return OrderType.NONE_ORDER
        high3 = self.ohlcv.values['high'][idx - 3]
        low0 = self.ohlcv.values['low'][idx]
        low1 = self.ohlcv.values['low'][idx - 1]
        high1 = self.ohlcv.values['high'][idx - 1]
        high2 = self.ohlcv.values['high'][idx - 2]
        close0 = self.ohlcv.values['close'][idx]
        close1 = self.ohlcv.values['close'][idx - 1]
        short_flg1 = high3 < low0
        short_flg2 = low0 < high1
        short_flg3 = high1 < high2
        short_flg4 = close0 < close1
        if short_flg1 and short_flg2 and short_flg3 and short_flg4:
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

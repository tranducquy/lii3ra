from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class BackInStyleFactory(EntryStrategyFactory):
    params = {
    }

    rough_params = [
    ]

    def create_strategy(self, ohlcv):
        return BackInStyle(ohlcv)

    def optimization(self, ohlcv, rough=True):
        return [BackInStyle(ohlcv)]


class BackInStyle(EntryStrategy):
    """
    BACK IN STYLE
    """

    def __init__(self
                 , ohlcv
                 , order_vol_ratio=0.01):
        self.title = f"BackInStyle"
        self.ohlcv = ohlcv
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def check_entry_long(self, idx, last_exit_idx):
        """
        long_flg1 = highs[idx-3] < lows[idx]
        long_flg2 = lows[idx] < highs[idx-1]
        long_flg3 = highs[idx] < highs[idx-2]
        long_flg4 = highs[idx-1] < highs[idx-2]
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= 3:
            return OrderType.NONE_ORDER
        highs = self.ohlcv.values['high']
        lows = self.ohlcv.values['low']
        long_flg1 = highs[idx - 3] < lows[idx]
        long_flg2 = lows[idx] < highs[idx - 1]
        long_flg3 = highs[idx] < highs[idx - 2]
        long_flg4 = highs[idx - 1] < highs[idx - 2]
        if long_flg1 and long_flg2 and long_flg3 and long_flg4:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        short_flg1 = lows[idx-3] > highs[idx]
        short_flg2 = highs[idx] > lows[idx-1]
        short_flg3 = lows[idx] > lows[idx-2]
        short_flg4 = lows[idx-1] > lows[idx-2]
        3バー前の安値が現在の高値よりも大きく、
        現在の高値が前の安値よりも大きく、
        現在の安値が2バー前の安値よりも大きく、
        前の安値が2バー前の安値よりも大きい場合、ショートする。
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= 3:
            return OrderType.NONE_ORDER
        highs = self.ohlcv.values['high']
        lows = self.ohlcv.values['low']
        short_flg1 = lows[idx - 3] > highs[idx]
        short_flg2 = highs[idx] > lows[idx - 1]
        short_flg3 = lows[idx] > lows[idx - 2]
        short_flg4 = lows[idx - 1] > lows[idx - 2]
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

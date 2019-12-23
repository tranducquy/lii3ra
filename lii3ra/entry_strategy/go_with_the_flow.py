from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategy
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory


class GoWithTheFlowFactory(EntryStrategyFactory):
    params = {
        # NOTHING
    }

    rough_params = [
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        return GoWithTheFlow(ohlcv)

    def optimization(self, ohlcv, rough=True):
        strategies = [GoWithTheFlow(ohlcv)]
        return strategies


class GoWithTheFlow(EntryStrategy):
    """
    GO WITH THE FLOW
    """
    def __init__(self
                 , ohlcv
                 , order_vol_ratio=0.01):
        self.title = f"GoWithTheFlow"
        self.ohlcv = ohlcv
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def check_entry_long(self, idx, last_exit_idx):
        """
        現在の終値が前の終値よりも高い場合、成行でロング
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= 1:
            return OrderType.NONE_ORDER
        close0 = self.ohlcv.values['close'][idx]
        close1 = self.ohlcv.values['close'][idx-1]
        condition1 = close1 < close0
        if condition1:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        現在の終値が前の終値よりも安い場合、成行でショート
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= 1:
            return OrderType.NONE_ORDER
        close0 = self.ohlcv.values['close'][idx]
        close1 = self.ohlcv.values['close'][idx-1]
        condition1 = close1 > close0
        if condition1:
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

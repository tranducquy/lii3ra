from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class ClosingPatternOnlyFactory(EntryStrategyFactory):
    params = {
    }

    rough_params = [
    ]

    def create_strategy(self, ohlcv):
        return ClosingPatternOnly(ohlcv)

    def optimization(self, ohlcv, rough=True):
        strategies = [ClosingPatternOnly(ohlcv)]
        return strategies


class ClosingPatternOnly(EntryStrategy):
    """
    CLOSING PATTERN ONLY
    ロング:前の終値は3つ前の終値よりも大きく、現在の終値は2つ前の終値よりも大きく、2つ前は1つ前よりも大きい。
    ショートトレード：すべての「>」を「<」で変更します
    """

    def __init__(self
                 , ohlcv
                 , order_vol_ratio=0.01):
        self.title = f"ClosingPatternOnly"
        self.ohlcv = ohlcv
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def check_entry_long(self, idx, last_exit_idx):
        """
if c[1]>c[3] and c>c[2] and c[2]>c[1] then buy next bar at market;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= 3:
            return OrderType.NONE_ORDER
        close0 = self.ohlcv.values['close'][idx]
        close1 = self.ohlcv.values['close'][idx - 1]
        close2 = self.ohlcv.values['close'][idx - 2]
        close3 = self.ohlcv.values['close'][idx - 3]
        long_flg1 = close1 > close3
        long_flg2 = close0 > close2
        long_flg3 = close2 > close1
        if long_flg1 and long_flg2 and long_flg3:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
If c[1]<c[3] and c<c[2] and c[2]<c[1] then Sell short next bar at market;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= 3:
            return OrderType.NONE_ORDER
        close0 = self.ohlcv.values['close'][idx]
        close1 = self.ohlcv.values['close'][idx - 1]
        close2 = self.ohlcv.values['close'][idx - 2]
        close3 = self.ohlcv.values['close'][idx - 3]
        short_flg1 = close1 < close3
        short_flg2 = close0 < close2
        short_flg3 = close2 < close1
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

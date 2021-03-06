from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.simple_movingaverage import SimpleMovingAverage
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class BooksCanBeGreatFactory(EntryStrategyFactory):
    params = {
        # fast_sma_span, slow_sma_span
        "default": [5, 10]
        # , "^N225": [3, 1.0, 3, 1.0]
    }

    def create(self, ohlcv, optimization=False):
        strategies = []
        if not optimization:
            #
            s = ohlcv.symbol
            if s in self.params:
                fast_sma_span = self.params[s][0]
                slow_sma_span = self.params[s][1]
            else:
                fast_sma_span = self.params["default"][0]
                slow_sma_span = self.params["default"][1]
            strategies.append(BooksCanBeGreat(ohlcv, fast_sma_span, slow_sma_span))
        else:
            fast_spans = [i for i in range(3, 10, 2)]
            slow_spans = [i for i in range(10, 30, 4)]
            for fast_span in fast_spans:
                for slow_span in slow_spans:
                    strategies.append(BooksCanBeGreat(ohlcv, fast_span, slow_span))
        return strategies


class BooksCanBeGreat(EntryStrategy):
    """
    BOOKS CAN BE GREAT
    """

    def __init__(self
                 , ohlcv
                 , fast_sma_span
                 , slow_sma_span
                 , order_vol_ratio=0.01):
        self.title = f"BooksCanBeGreat[{fast_sma_span:.0f},{slow_sma_span:.0f}]"
        self.ohlcv = ohlcv
        self.fast_sma = SimpleMovingAverage(ohlcv, fast_sma_span)
        self.slow_sma = SimpleMovingAverage(ohlcv, slow_sma_span)
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.fast_sma.sma[idx] == 0
                or self.slow_sma.sma[idx] == 0
        ):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        """
        短期SMAが長期SMAを上から下に抜けてクロスした直後に現在の終値が短期SMAより下にある場合、次のバーで新規成行買
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.slow_sma.sma_span:
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        fast_sma_before = self.fast_sma.sma[idx - 1]
        fast_sma_current = self.fast_sma.sma[idx]
        slow_sma_before = self.slow_sma.sma[idx - 1]
        slow_sma_current = self.slow_sma.sma[idx]
        cross_condition = fast_sma_before > slow_sma_before and fast_sma_current < slow_sma_current
        close_condition = close < fast_sma_current
        if cross_condition and close_condition:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        短期SMAが長期SMAを下から上に抜けてクロスした直後に現在の終値が短期SMAより上にある場合、次のバーで新規成行売
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.slow_sma.sma_span:
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        fast_sma_before = self.fast_sma.sma[idx - 1]
        fast_sma_current = self.fast_sma.sma[idx]
        slow_sma_before = self.slow_sma.sma[idx - 1]
        slow_sma_current = self.slow_sma.sma[idx]
        cross_condition = fast_sma_before > slow_sma_before and fast_sma_current < slow_sma_current
        close_condition = close > fast_sma_current
        if cross_condition and close_condition:
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
        ind1 = self.fast_sma.sma[idx]
        ind2 = self.slow_sma.sma[idx]
        ind3 = None
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

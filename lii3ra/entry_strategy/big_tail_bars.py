from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class BigTailBars(EntryStrategy):
    """
    ブルテールが多い場合はロング、ベアテールが多い場合はショートする
    """

    def __init__(self
                 , title
                 , ohlcv
                 , lookback_period
                 , threshold
                 , order_vol_ratio=0.01):
        self.title = title
        self.ohlcv = ohlcv
        self.lookback_period = lookback_period
        self.threshold = threshold
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio
        self._bullbar_cnt = 0
        self._bearbar_cnt = 0

    def check_entry_long(self, idx, last_exit_idx):
        """
        ブルテールが多い場合はロングする
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.lookback_period:
            return OrderType.NONE_ORDER
        (bullbar, bearbar) = self._get_bull_bear(idx)
        bull_flg = bullbar > bearbar and bullbar > self.threshold
        if bull_flg:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        ベアテールが多い場合はショートする
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.lookback_period:
            return OrderType.NONE_ORDER
        (bullbar, bearbar) = self._get_bull_bear(idx)
        bear_flg = bullbar < bearbar and bearbar > self.threshold
        if bear_flg:
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
        ind1 = self._bullbar_cnt
        ind2 = self._bearbar_cnt
        ind3 = self.threshold
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

    def _get_bull_bear(self, idx):
        bullbar_cnt = 0
        bearbar_cnt = 0
        for i in range(self.lookback_period):
            open_price = self.ohlcv.values['open'][idx - i]
            high = self.ohlcv.values['high'][idx - i]
            low = self.ohlcv.values['low'][idx - i]
            close = self.ohlcv.values['close'][idx - i]
            high_before = self.ohlcv.values['high'][idx - i - 1]
            low_before = self.ohlcv.values['low'][idx - i - 1]
            bullbar = close > open_price and (open_price - low) > (close - open_price) and high > high_before
            if bullbar:
                bullbar_cnt += 1
            bearbar = close < open_price and (high - open_price) > (open_price - close) and low < low_before
            if bearbar:
                bearbar_cnt += 1
        self._bullbar_cnt = bullbar_cnt
        self._bearbar_cnt = bearbar_cnt
        return bullbar_cnt, bearbar_cnt

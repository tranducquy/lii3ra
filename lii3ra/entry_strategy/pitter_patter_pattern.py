from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class PitterPatterPattern(EntryStrategy):
    """
    PITTER PATTER PATTERN
    ロング：前回のオープン>現在の高値と現在のオープン値>前回の終値と前回のクローズ値
    ショート：すべての「高」を「低」に、すべての「>」を「<」に変更
    """
    def __init__(self
                , title
                , ohlcv
                , order_vol_ratio=0.01):
        self.title                 = title
        self.ohlcv                 = ohlcv
        self.symbol                = self.ohlcv.symbol
        self.order_vol_ratio       = order_vol_ratio
    
    def check_entry_long(self, idx, last_exit_idx):
        """
If o[1] > h[0] AND o[0] > c[1] AND c[1] > l[1] AND l[1] > c[0] then buy next bar at market;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= 1:
            return OrderType.NONE_ORDER
        before_open = self.ohlcv.values['open'][idx-1]
        current_high = self.ohlcv.values['high'][idx]
        current_open = self.ohlcv.values['open'][idx]
        before_close = self.ohlcv.values['close'][idx-1]
        current_close = self.ohlcv.values['close'][idx]
        before_low = self.ohlcv.values['low'][idx-1]
        long_flg1 = before_open > current_high
        long_flg2 = current_open > before_close
        long_flg3 = before_close > before_low
        long_flg4 = before_low > current_close
        if long_flg1 and long_flg2 and long_flg3 and long_flg4:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
if l o[1] < l[0] AND o[0] < c[1] AND c[1] < h[1] AND h[1] < c[0] then sell short next bar at market;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= 1:
            return OrderType.NONE_ORDER
        before_open = self.ohlcv.values['open'][idx-1]
        current_low = self.ohlcv.values['low'][idx]
        current_open = self.ohlcv.values['open'][idx]
        before_close = self.ohlcv.values['close'][idx-1]
        before_high = self.ohlcv.values['high'][idx-1]
        current_close = self.ohlcv.values['close'][idx]
        short_flg1 = before_open < current_low
        short_flg2 = current_open < before_close
        short_flg3 = before_close < before_high
        short_flg4 = before_close < current_close
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

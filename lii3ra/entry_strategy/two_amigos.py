from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class TwoAmigos(EntryStrategy):
    """
    ADX、短期および長期のモメンタムを使用してエントリーする。
    最適化しすぎないほうが良いらしい。
    """
    def __init__(self
                 , title
                 , ohlcv
                 , adx
                 , adx_threshold
                 , lookback
                 , order_vol_ratio=0.01):
        self.title = title
        self.ohlcv = ohlcv
        self.symbol = self.ohlcv.symbol
        self.adx = adx
        self.adx_threshold = adx_threshold
        self.lookback = lookback
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.adx.adx[idx] == 0
        ):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        """
        ADXが閾値を上回っており、モメンタムが上昇トレンドであれば次で成行ロング
vars: ADXLength(14), lookback(20);
If ADX(ADXLength)>20 then begin
    If close>close[lookback] then buy next bar at market;
    If close<close[lookback] then sellshort next bar at market;
end;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.adx.adx_span \
                or idx <= self.lookback:
            return OrderType.NONE_ORDER
        if self.adx.adx[idx] > self.adx_threshold:
            close = self.ohlcv.values['close'][idx]
            close_lookback = self.ohlcv.values['close'][idx-self.lookback]
            lookback_condition = close > close_lookback
            if lookback_condition:
                return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        ADXが閾値を上回っており、モメンタムが下降トレンドであれば次で成行ショート
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.adx.adx_span \
                or idx <= self.lookback:
            return OrderType.NONE_ORDER
        if self.adx.adx[idx] > self.adx_threshold:
            close = self.ohlcv.values['close'][idx]
            close_lookback = self.ohlcv.values['close'][idx-self.lookback]
            lookback_condition = close < close_lookback
            if lookback_condition:
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
        ind1 = self.adx.adx[idx]
        ind2 = self.adx_threshold
        ind3 = self.ohlcv.values['close'][idx-self.lookback] if idx > self.lookback else None
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

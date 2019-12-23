from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class ClassicKeltnerChannel(EntryStrategy):
    """
    終値がボリンジャーバンドをクロスし、モメンタムのトレンドと一致していればエントリーする
vars: Length( 20 ), NumATRs( 2 ), Length2(10);
vars: LowerBand( 0 ), UpperBand(0);
LowerBand = Average(close,Length)-NumATRs*AvgTrueRange(Length);
UpperBand = Average(close,Length)+NumATRs*AvgTrueRange(Length) ;
if Close crosses over LowerBand and close>close[Length2] then Buy next bar at market;
if Close crosses under UpperBand and close<close[Length2] then SellShort next bar at market;
    """

    def __init__(self, title, ohlcv, kc, lookback, order_vol_ratio=0.01):
        self.title = title
        self.ohlcv = ohlcv
        self.kc = kc
        self.lookback = lookback
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.kc.lower_band[idx] == 0
                or self.kc.upper_band[idx] == 0):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        """
        終値がバンドをクロスして、モメンタムが上昇トレンドならロング
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.kc.atr_span:
            return OrderType.NONE_ORDER
        before_close = self.ohlcv.values['close'][idx-self.lookback]
        current_close = self.ohlcv.values['close'][idx]
        momentum = before_close < current_close
        before_condition = current_close < self.kc.lower_band[idx-1]
        current_condition = current_close > self.kc.lower_band[idx]
        if before_condition and current_condition and momentum:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        終値がバンドをクロスして、モメンタムが下降トレンドならロング
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.kc.atr_span:
            return OrderType.NONE_ORDER
        before_close = self.ohlcv.values['close'][idx-self.lookback]
        current_close = self.ohlcv.values['close'][idx]
        momentum = before_close > current_close
        before_condition = current_close > self.kc.upper_band[idx-1]
        current_condition = current_close < self.kc.upper_band[idx]
        if before_condition and current_condition and momentum:
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
        price = self.ohlcv.values['high'][idx] + self.tick
        return price

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        price = self.ohlcv.values['low'][idx] - self.tick
        return price

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
        ind1 = self.kc.middle[idx]
        ind2 = self.kc.upper_band[idx]
        ind3 = self.kc.lower_band[idx]
        ind4 = self.ohlcv.values['close'][idx-self.lookback] if idx > self.lookback else None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7





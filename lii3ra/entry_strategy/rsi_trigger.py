from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class RSITrigger(EntryStrategy):
    """
    RSIがRSI Thresholdを下回っていて、終値が終値のEMAを下回っている場合、次のバーでロングを成行注文する
    RSIが100-RSI Thresholdを上回っていて、終値が終値のEMAを上回っている場合、次のバーでショートを成行注文する
    """
    def __init__(self
                 , title
                 , ohlcv
                 , rsi
                 , rsi_threshold
                 , ema
                 , order_vol_ratio=0.01):
        self.title = title
        self.ohlcv = ohlcv
        self.symbol = self.ohlcv.symbol
        self.rsi = rsi
        self.rsi_threshold = rsi_threshold
        self.ema = ema
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.rsi.rsi[idx] == 0
                or self.ema.ema[idx] == 0
        ):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        """
        当日RSIがRSI Thresholdを下回っておりEMAを上回っている場合、次のバーで成行買
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        current_rsi = self.rsi.rsi[idx]
        current_ema = self.ema.ema[idx]
        rsi_flg = current_rsi < self.rsi_threshold
        ema_flg = current_ema < close
        if rsi_flg and ema_flg:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        当日RSIが100-RSI Thresholdを上回っており終値がEMAを下回っている場合、次のバーで成行買
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        current_rsi = self.rsi.rsi[idx]
        current_ema = self.ema.ema[idx]
        rsi_flg = current_rsi > (100 - self.rsi_threshold)
        ema_flg = current_ema > close
        if rsi_flg and ema_flg:
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
        ind1 = self.ema.ema[idx]
        ind2 = self.rsi.rsi[idx]
        ind3 = self.rsi_threshold
        ind4 = (100 - self.rsi_threshold)
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

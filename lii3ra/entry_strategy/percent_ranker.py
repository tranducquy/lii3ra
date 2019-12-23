import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class PercentRanker(EntryStrategy):
    """
    現在の終値が直近の終値のパーセンタイルの安値または高値に位置する場合に
    ADXのトレンドに基づき次のバーでエントリーする。
    """

    def __init__(self
                 , title
                 , ohlcv
                 , percentile_lookback_span
                 , long_percentile_ratio
                 , long_adx
                 , long_adx_ratio1
                 , long_adx_ratio2
                 , short_percentile_ratio
                 , short_adx
                 , short_adx_ratio1
                 , short_adx_ratio2
                 , order_vol_ratio=0.01):
        self.title = title
        self.ohlcv = ohlcv
        self.percentile_lookback_span = percentile_lookback_span
        self.long_percentile_ratio = long_percentile_ratio
        self.long_adx = long_adx
        self.long_adx_ratio1 = long_adx_ratio1
        self.long_adx_ratio2 = long_adx_ratio2
        self.short_percentile_ratio = short_percentile_ratio
        self.short_adx = short_adx
        self.short_adx_ratio1 = short_adx_ratio1
        self.short_adx_ratio2 = short_adx_ratio2
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.long_adx.adx[idx] == 0
                or self.short_adx.adx[idx] == 0
        ):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        """
        当日終値がパーセンタイルの指定レンジ内にあり、ADXのトレンド範囲内である場合、次のバーで新規成行買
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        percentile_value = self._calc_percentile(idx, self.percentile_lookback_span, self.long_percentile_ratio)
        close = self.ohlcv.values['close'][idx]
        long_adx_flg1 = self.long_adx.adx[idx] > self.long_adx_ratio1
        long_adx_flg2 = self.long_adx.adx[idx] < self.long_adx_ratio2
        long_value_flg = close > percentile_value
        if long_adx_flg1 and long_adx_flg2 and long_value_flg:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        当日終値がパーセンタイルの指定レンジ内にあり、ADXのトレンド範囲内である場合、次のバーで新規成行売
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        percentile_value = self._calc_percentile(idx, self.percentile_lookback_span, self.short_percentile_ratio)
        close = self.ohlcv.values['close'][idx]
        short_adx_flg1 = self.short_adx.adx[idx] > self.short_adx_ratio1
        short_adx_flg2 = self.short_adx.adx[idx] < self.short_adx_ratio2
        short_value_flg = close < percentile_value
        if short_adx_flg1 and short_adx_flg2 and short_value_flg:
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
        ind1 = self._percentile_value
        ind2 = self.long_adx.adx[idx]
        ind3 = self.long_adx_ratio1
        ind4 = self.long_adx_ratio2
        ind5 = self.short_adx.adx[idx]
        ind6 = self.short_adx_ratio1
        ind7 = self.short_adx_ratio2
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

    def _calc_percentile(self, idx, span, q):
        origin = idx - span + 1 if idx - span > 0 else idx
        prices = self.ohlcv.values['close'][origin:idx + 1]
        self._percentile_value = np.nanpercentile(prices, q)
        return self._percentile_value

import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.average_directional_index import AverageDirectionalIndex
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class BreakoutWithTwistFactory(EntryStrategyFactory):
    params = {
        # long_lookback_span, long_adx_span, long_adx_value, short_lookback_span, short_adx_span, short_adx_value
        "default": [10, 15, 0.2, 10, 15, 0.2]
        , "^N225": [10, 24, 0.3, 10, 6, 0.5]
    }

    rough_params = [
        [10, 15, 0.3, 0, 1, 0]
        , [10, 15, 0.7, 0, 1, 0]
        , [10, 25, 0.3, 0, 1, 0]
        , [10, 25, 0.7, 0, 1, 0]
        , [60, 15, 0.3, 0, 1, 0]
        , [60, 25, 0.3, 0, 1, 0]
        , [60, 15, 0.7, 0, 1, 0]
        , [60, 25, 0.7, 0, 1, 0]
        , [130, 15, 0.3, 0, 1, 0]
        , [130, 25, 0.3, 0, 1, 0]
        , [130, 15, 0.7, 0, 1, 0]
        , [130, 25, 0.7, 0, 1, 0]
        , [0, 1, 0, 10, 6, 0.40]
        , [0, 1, 0, 10, 14, 0.40]
        , [0, 1, 0, 10, 6, 0.70]
        , [0, 1, 0, 10, 14, 0.70]
        , [0, 1, 0, 60, 6, 0.40]
        , [0, 1, 0, 60, 14, 0.40]
        , [0, 1, 0, 60, 6, 0.70]
        , [0, 1, 0, 60, 14, 0.70]
        , [0, 1, 0, 130, 6, 0.40]
        , [0, 1, 0, 130, 14, 0.40]
        , [0, 1, 0, 130, 6, 0.70]
        , [0, 1, 0, 130, 14, 0.70]
        # , [10, 15, 0.3, 10, 15, 0.3]
        # , [60, 15, 0.4, 60, 15, 0.4]
        # , [130, 15, 0.7, 130, 15, 0.7]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            long_lookback_span = self.params[s][0]
            long_adx_span = self.params[s][1]
            long_adx_value = self.params[s][2]
            short_lookback_span = self.params[s][3]
            short_adx_span = self.params[s][4]
            short_adx_value = self.params[s][5]
        else:
            long_lookback_span = self.params["default"][0]
            long_adx_span = self.params["default"][1]
            long_adx_value = self.params["default"][2]
            short_lookback_span = self.params["default"][3]
            short_adx_span = self.params["default"][4]
            short_adx_value = self.params["default"][5]
        return BreakoutWithTwist(ohlcv, long_lookback_span, long_adx_span, long_adx_value
                                 , short_lookback_span, short_adx_span, short_adx_value)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            for p in self.rough_params:
                strategies.append(BreakoutWithTwist(ohlcv
                                                    , p[0]
                                                    , p[1]
                                                    , p[2]
                                                    , p[3]
                                                    , p[4]
                                                    , p[5]))
        else:
            lookback_span_list = [10, 25, 60, 120, 240]
            adx_span_list = [i for i in range(5, 26, 5)]
            adx_value_list = [0.30, 0.40, 0.50, 0.60, 0.70]
            for lookback_span in lookback_span_list:
                for adx_span in adx_span_list:
                    for adx_value in adx_value_list:
                        strategies.append(BreakoutWithTwist(ohlcv, lookback_span, adx_span, adx_value
                                                            , 0, 1, 0))
            for lookback_span in lookback_span_list:
                for adx_span in adx_span_list:
                    for adx_value in adx_value_list:
                        strategies.append(BreakoutWithTwist(ohlcv, 0, 1, 0
                                                            , lookback_span, adx_span, adx_value))
        return strategies


class BreakoutWithTwist(EntryStrategy):
    """
    高値または安値が指定のバー数の高値を更新した場合に成行注文する
    """

    def __init__(self
                 , ohlcv
                 , long_lookback_span
                 , long_adx_span
                 , long_adx_value
                 , short_lookback_span
                 , short_adx_span
                 , short_adx_value
                 , order_vol_ratio=0.01):
        self.title = f"BreakoutTwist[{long_lookback_span:.0f},{long_adx_span:.0f},{long_adx_value:.2f}]"
        self.title += f"[{short_lookback_span:.0f},{short_adx_span:.0f},{short_adx_value:.2f}]"
        self.ohlcv = ohlcv
        self.long_lookback_span = long_lookback_span
        self.long_adx = AverageDirectionalIndex(ohlcv, long_adx_span)
        self.long_adx_value = long_adx_value
        self.short_lookback_span = short_lookback_span
        self.short_adx = AverageDirectionalIndex(ohlcv, short_adx_span)
        self.short_adx_value = short_adx_value
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
        当日高値が指定バー数分の高値を更新した場合、次のバーで成行買
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        max_high = self.ohlcv.values['high'][idx - self.long_lookback_span:idx].max()
        long_flg = max_high < self.ohlcv.values['high'][idx]
        long_adx_flg = self.long_adx.adx[idx] < self.long_adx_value
        if long_flg and long_adx_flg:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        当日安値が指定バー数分の安値を更新した場合、次のバーで成行売
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        min_low = self.ohlcv.values['low'][idx - self.short_lookback_span:idx].min()
        short_flg = min_low > self.ohlcv.values['low'][idx]
        short_adx_flg = self.short_adx.adx[idx] < self.short_adx_value
        if short_flg and short_adx_flg:
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
        ind1 = self.long_adx.adx[idx]
        ind2 = self.long_adx_value
        ind3 = self.long_lookback_span
        ind4 = self.short_adx.adx[idx]
        ind5 = self.short_adx_value
        ind6 = self.short_lookback_span
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

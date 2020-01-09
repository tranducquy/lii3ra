import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.average_directional_index import AverageDirectionalIndex
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class PercentRankerFactory(EntryStrategyFactory):
    params = {
        # percentile_lookback_span, long_percentile_ratio, long_adx_span, long_adx_ratio1, long_adx_ratio2, short_percentile_ratio, short_adx_span, short_adx_ratio1, short_adx_ratio2
        "default": [25, 75, 14, 0.20, 0.30, 25, 14, 0.20, 0.30]
        , "6141.T": [20, 60, 20, 0.20, 0.45, 30, 10, 0.20, 0.30]
    }

    rough_params = [
        [25, 75, 14, 0.20, 0.30, 25, 14, 0.20, 0.30]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            percentile_lookback_span = self.params[s][0]
            long_percentile_ratio = self.params[s][1]
            long_adx_span = self.params[s][2]
            long_adx_ratio1 = self.params[s][3]
            long_adx_ratio2 = self.params[s][4]
            short_percentile_ratio = self.params[s][5]
            short_adx_span = self.params[s][6]
            short_adx_ratio1 = self.params[s][7]
            short_adx_ratio2 = self.params[s][8]
        else:
            percentile_lookback_span = self.params["default"][0]
            long_percentile_ratio = self.params["default"][1]
            long_adx_span = self.params["default"][2]
            long_adx_ratio1 = self.params["default"][3]
            long_adx_ratio2 = self.params["default"][4]
            short_percentile_ratio = self.params["default"][5]
            short_adx_span = self.params["default"][6]
            short_adx_ratio1 = self.params["default"][7]
            short_adx_ratio2 = self.params["default"][8]
        return PercentRanker(ohlcv
                             , percentile_lookback_span
                             , long_percentile_ratio
                             , long_adx_span
                             , long_adx_ratio1
                             , long_adx_ratio2
                             , short_percentile_ratio
                             , short_adx_span
                             , short_adx_ratio1
                             , short_adx_ratio2)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            #
            for p in self.rough_params:
                strategies.append(PercentRanker(ohlcv
                                                , p[0]
                                                , p[1]
                                                , p[2]
                                                , p[3]
                                                , p[4]
                                                , p[5]
                                                , p[6]
                                                , p[7]
                                                , p[8]
                                                ))
        else:
            lookback_span_list = [5, 10, 15, 20]
            percentile_ratio_list = [30, 40, 50, 60, 70]
            adx_span_list = [5, 10, 15, 20]
            adx_ratio1_list = [0.20]
            adx_ratio2_list = [0.30, 0.45]
            for lookback in lookback_span_list:
                for percentile_ratio in percentile_ratio_list:
                    for adx_span in adx_span_list:
                        for adx_ratio1 in adx_ratio1_list:
                            for adx_ratio2 in adx_ratio2_list:
                                strategies.append(PercentRanker(ohlcv
                                                                , lookback
                                                                , percentile_ratio
                                                                , adx_span
                                                                , adx_ratio1
                                                                , adx_ratio2
                                                                , 0
                                                                , 1
                                                                , 0
                                                                , 0))
        for lookback in lookback_span_list:
            for percentile_ratio in percentile_ratio_list:
                for adx_span in adx_span_list:
                    for adx_ratio1 in adx_ratio1_list:
                        for adx_ratio2 in adx_ratio2_list:
                            strategies.append(PercentRanker(ohlcv
                                                            , lookback
                                                            , 0
                                                            , 1
                                                            , 0
                                                            , 0
                                                            , percentile_ratio
                                                            , adx_span
                                                            , adx_ratio1
                                                            , adx_ratio2))
        return strategies


class PercentRanker(EntryStrategy):
    """
    現在の終値が直近の終値のパーセンタイルの安値または高値に位置する場合に
    ADXのトレンドに基づき次のバーでエントリーする。
    """

    def __init__(self
                 , ohlcv
                 , percentile_lookback_span
                 , long_percentile_ratio
                 , long_adx_span
                 , long_adx_ratio1
                 , long_adx_ratio2
                 , short_percentile_ratio
                 , short_adx_span
                 , short_adx_ratio1
                 , short_adx_ratio2
                 , order_vol_ratio=0.01):
        self.title = f"PercentRanker[{percentile_lookback_span:.0f}][{long_percentile_ratio:.0f},{long_adx_span:.0f}" \
                     f",{long_adx_ratio1:.2f},{long_adx_ratio2:.2f}][{short_percentile_ratio:.0f},{short_adx_span:.0f}," \
                     f"{short_adx_ratio1:.2f},{short_adx_ratio2:.2f}]"
        self.ohlcv = ohlcv
        self.percentile_lookback_span = percentile_lookback_span
        self.long_percentile_ratio = long_percentile_ratio
        self.long_adx = AverageDirectionalIndex(ohlcv, long_adx_span)
        self.long_adx_ratio1 = long_adx_ratio1
        self.long_adx_ratio2 = long_adx_ratio2
        self.short_percentile_ratio = short_percentile_ratio
        self.short_adx = AverageDirectionalIndex(ohlcv, short_adx_span)
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

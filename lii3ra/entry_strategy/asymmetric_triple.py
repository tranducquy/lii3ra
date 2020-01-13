import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.average_true_range import AverageTrueRange
from lii3ra.technical_indicator.triangular_movingaverage import TriangularMovingAverage
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class AsymmetricTripleFactory(EntryStrategyFactory):
    params = {
        # atr_span, atr_mult, trima_span, lookback_span
        "default": [15, 0.5, 10, 10]
        , "^N225": [10, 0.3, 25, 10]
        # , "6753.T": [25, 0.3, 5, 15]
        , "6753.T": [15, 0.3, 15, 15]
        , "1570.T": [5, 0.3, 10, 5]
        , "7974.T": [20, 0.3, 20, 10]
        , "9107.T": [15, 0.3, 10, 15]
        , "9104.T": [20, 0.3, 5, 5]
        , "9007.T": [15, 0.5, 10, 10]
    }

    rough_params = [
        [5, 0.3, 10, 5]
        , [10, 0.3, 20, 10]
        , [10, 0.3, 25, 10]
        , [15, 0.5, 10, 10]
        , [20, 0.3, 10, 10]
        , [25, 0.3, 5, 15]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            atr_span = self.params[s][0]
            atr_mult = self.params[s][1]
            trima_span = self.params[s][2]
            lookback_span = self.params[s][3]
        else:
            atr_span = self.params["default"][0]
            atr_mult = self.params["default"][1]
            trima_span = self.params["default"][2]
            lookback_span = self.params["default"][3]
        return AsymmetricTriple(ohlcv, atr_span, atr_mult, trima_span, lookback_span)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            for p in self.rough_params:
                strategies.append(AsymmetricTriple(ohlcv
                                                   , p[0]
                                                   , p[1]
                                                   , p[2]
                                                   , p[3]))
        else:
            atr_spans = [i for i in range(5, 21, 5)]
            atr_mults = [i for i in np.arange(0.3, 1.6, 0.3)]
            trima_spans = [i for i in range(5, 21, 5)]
            lookback_spans = [i for i in range(5, 16, 5)]
            for atr_span in atr_spans:
                for atr_mult in atr_mults:
                    for trima_span in trima_spans:
                        for lookback_span in lookback_spans:
                            strategies.append(AsymmetricTriple(ohlcv, atr_span, atr_mult, trima_span, lookback_span))
        return strategies


class AsymmetricTriple(EntryStrategy):
    """
    安値の三角移動平均でエントリーを判定し、ATRを用いて逆指値注文する
    """
    def __init__(self
                 , ohlcv
                 , atr_span
                 , atr_mult
                 , trima_span
                 , lookback_span
                 , order_vol_ratio=0.01):
        self.title = f"AsymTriple[{atr_span:.0f},{atr_mult:.1f},{trima_span:.0f},{lookback_span:.0f}]"
        self.ohlcv = ohlcv
        self.atr = AverageTrueRange(ohlcv, atr_span)
        self.atr_mult = atr_mult
        self.trima = TriangularMovingAverage(ohlcv, trima_span)
        self.lookback_span = lookback_span
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.atr.atr[idx] == 0
                or self.trima.trima_low[idx] == 0
        ):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        """
        安値の三角移動平均が指定日の安値よりも高い場合は逆指値でロングのエントリー
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.lookback_span or idx <= self.atr.atr_span:
            return OrderType.NONE_ORDER
        value1 = self.trima.trima_low[idx]
        value2 = self.ohlcv.values['low'][idx - self.lookback_span]
        if not np.isnan(value1) and not np.isnan(value2) and value1 >= value2:
            return OrderType.STOP_MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        安値の三角移動平均が指定日の安値よりも安い場合は逆指値でショートのエントリー
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.lookback_span or idx <= self.atr.atr_span:
            return OrderType.NONE_ORDER
        value1 = self.trima.trima_low[idx]
        value2 = self.ohlcv.values['low'][idx - self.lookback_span]
        if np.isnan(value1) or np.isnan(value2) or value1 >= value2:
            return OrderType.NONE_ORDER
        else:
            return OrderType.STOP_MARKET_SHORT

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
        close = self.ohlcv.values['close'][idx]
        price = close + self.atr_mult * self.atr.atr[idx]
        return price

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        low = self.ohlcv.values['low'][idx]
        price = low - self.atr_mult * self.atr.atr[idx]
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
        ind1 = self.trima.trima[idx]
        ind2 = self.trima.trima_low[idx]
        ind3 = self.atr.atr[idx]
        ind4 = self.ohlcv.values['close'][idx] + self.atr.atr[idx] * self.atr_mult
        ind5 = self.ohlcv.values['low'][idx] - self.atr.atr[idx] * self.atr_mult
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7


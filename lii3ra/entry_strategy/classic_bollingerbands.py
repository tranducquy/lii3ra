import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.bollingerband import Bollingerband
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class ClassicBollingerbandsFactory(EntryStrategyFactory):
    params = {
        # bb_period, sigma1_ratio, lookback
        "default": [20, 2.0, 10]
    }

    def create(self, ohlcv, optimization=False):
        strategies = []
        if not optimization:
            s = ohlcv.symbol
            if s in self.params:
                bb_period = self.params[s][0]
                sigma1_ratio = self.params[s][1]
                lookback = self.params[s][2]
            else:
                bb_period = self.params["default"][0]
                sigma1_ratio = self.params["default"][1]
                lookback = self.params["default"][2]
            strategies.append(ClassicBollingerbands(ohlcv, bb_period, sigma1_ratio, lookback))
        else:
            bb_period_ary = [i for i in range(5, 25, 5)]
            sigma1_ratio_ary = [i for i in np.arange(0.3, 2.0, 0.2)]
            lookback_ary = [i for i in range(5, 25, 5)]
            for bb_period in bb_period_ary:
                for sigma1_ratio in sigma1_ratio_ary:
                    for lookback in lookback_ary:
                        strategies.append(ClassicBollingerbands(ohlcv, bb_period, sigma1_ratio, lookback))
        return strategies


class ClassicBollingerbands(EntryStrategy):
    """
    終値がボリンジャーバンドをクロスし、モメンタムのトレンドと一致していればエントリーする
vars: Length( 20 ), NumDevs( 2 ), Length2(10);
vars: LowerBand( 0 ), UpperBand(0);
LowerBand = BollingerBand( Close, Length, -NumDevs ) ;
UpperBand = BollingerBand( Close, Length, +NumDevs ) ;
if Close crosses over LowerBand and close>close[Length2] then Buy next bar at market;
if Close crosses under UpperBand and close<close[Length2] then SellShort next bar at market;
    """

    def __init__(self,  ohlcv, bb_period, sigma1_ratio, lookback, order_vol_ratio=0.01):
        self.title = f"ClassicBollingerBands[{bb_period:.0f},{sigma1_ratio:.2f},{lookback:.0f}]"
        self.ohlcv = ohlcv
        self.bb = Bollingerband(ohlcv, bb_period, sigma1_ratio)
        self.lookback = lookback
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.bb.upper_sigma1[idx] == 0
                or self.bb.lower_sigma1[idx] == 0):
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
        if idx <= self.bb.span:
            return OrderType.NONE_ORDER
        if idx <= self.lookback:
            return OrderType.NONE_ORDER
        before_close = self.ohlcv.values['close'][idx-self.lookback]
        current_close = self.ohlcv.values['close'][idx]
        momentum = before_close < current_close
        before_condition = current_close < self.bb.lower_sigma1[idx-1]
        current_condition = current_close > self.bb.lower_sigma1[idx]
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
        if idx <= self.bb.span:
            return OrderType.NONE_ORDER
        if idx <= self.lookback:
            return OrderType.NONE_ORDER
        before_close = self.ohlcv.values['close'][idx-self.lookback]
        current_close = self.ohlcv.values['close'][idx]
        momentum = before_close > current_close
        before_condition = current_close > self.bb.upper_sigma1[idx-1]
        current_condition = current_close < self.bb.upper_sigma1[idx]
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
        ind1 = self.bb.sma[idx]
        ind2 = self.bb.upper_sigma1[idx]
        ind3 = self.bb.lower_sigma1[idx]
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7





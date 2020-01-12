import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.ultimate_oscillator import UltimateOscillator
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class TheUltimateFactory(EntryStrategyFactory):
    params = {
        # lookback, ultimate_avg1, ultimate_avg2, ultimate_avg3
        "default": [10, 7, 14, 28]
        , "3088.T": [10, 7, 14, 28]
        , "6619.T": [15, 7, 16, 28]
    }

    rough_params = [
        [5, 3, 6, 12]
        , [10, 7, 14, 28]
        , [15, 10, 20, 40]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            lookback = self.params[s][0]
            ultimate_avg1 = self.params[s][1]
            ultimate_avg2 = self.params[s][2]
            ultimate_avg3 = self.params[s][3]
        else:
            lookback = self.params["default"][0]
            ultimate_avg1 = self.params["default"][1]
            ultimate_avg2 = self.params["default"][2]
            ultimate_avg3 = self.params["default"][3]
        return TheUltimate(ohlcv, lookback, ultimate_avg1, ultimate_avg2, ultimate_avg3)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            for p in self.rough_params:
                strategies.append(TheUltimate(ohlcv
                                              , p[0]
                                              , p[1]
                                              , p[2]
                                              , p[3]))
        else:
            lookback_list = [i for i in range(5, 25, 5)]
            ultimate_avg1_list = [i for i in range(7, 8, 2)]
            ultimate_avg2_list = [i for i in range(14, 17, 2)]
            ultimate_avg3_list = [i for i in range(28, 29, 2)]
            for lookback in lookback_list:
                for ultimate_avg1 in ultimate_avg1_list:
                    for ultimate_avg2 in ultimate_avg2_list:
                        for ultimate_avg3 in ultimate_avg3_list:
                            strategies.append(TheUltimate(ohlcv, lookback, ultimate_avg1, ultimate_avg2, ultimate_avg3))
        return strategies


class TheUltimate(EntryStrategy):
    """
    THE ULTIMATE
     - 注文方法:寄成
    """
    def __init__(self
                 , ohlcv
                 , lookback
                 , ultimate_avg1
                 , ultimate_avg2
                 , ultimate_avg3
                 , order_vol_ratio=0.01):
        self.title = f"TheUltimate[{lookback:.0f},{ultimate_avg1:.0f},{ultimate_avg2:.0f},{ultimate_avg3:.0f}]"
        self.ohlcv = ohlcv
        self.symbol = self.ohlcv.symbol
        self.lookback = lookback
        self.uo = UltimateOscillator(ohlcv, ultimate_avg1, ultimate_avg2, ultimate_avg3)
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.uo.uo[idx] == 0
                or np.isnan(self.uo.uo[idx])
                or self.uo.uo[idx] is None
        ):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        """
Var: xbars(10);
if UltimateOsc(7,14,28)= lowest(UltimateOsc(7,14,28),xbars) then buy next bar at market;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.uo.avg3:
            return OrderType.NONE_ORDER
        uo_value = self.uo.uo[idx]
        lowest_uo_value = self.uo.uo[idx-self.lookback:idx+1].min()
        if uo_value == lowest_uo_value:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
Var: xbars(10);
if UltimateOsc(7,14,28)= highest(UltimateOsc(7,14,28),xbars) then sellshort next bar at market;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.uo.avg3:
            return OrderType.NONE_ORDER
        uo_value = self.uo.uo[idx]
        highest_uo_value = self.uo.uo[idx-self.lookback:idx+1].max()
        if uo_value == highest_uo_value:
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
        ind1 = self.uo.uo[idx]
        ind2 = None
        ind3 = None
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

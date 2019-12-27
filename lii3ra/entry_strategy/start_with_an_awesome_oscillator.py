import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.awesome_oscillator import AwesomeOscillator
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class StartWithAwesomeOscillatorFactory(EntryStrategyFactory):
    params = {
        # slow_period, fast_period, aback, bback, fatr
        "default": [7, 5, 5, 7, 0.5]
    }

    rough_params = [
        [7, 5, 5, 7, 0.5]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            slow_period = self.params[s][0]
            fast_period = self.params[s][1]
            aback = self.params[s][2]
            bback = self.params[s][3]
            fatr = self.params[s][4]
        else:
            slow_period = self.params["default"][0]
            fast_period = self.params["default"][1]
            aback = self.params["default"][2]
            bback = self.params["default"][3]
            fatr = self.params["default"][4]
        return StartWithAwesomeOscillator(ohlcv, slow_period, fast_period, aback, bback, fatr)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            for p in self.rough_params:
                strategies.append(StartWithAwesomeOscillator(ohlcv
                                                             , p[0]
                                                             , p[1]
                                                             , p[2]
                                                             , p[3]
                                                             , p[4]))
        else:
            slow_list = [i for i in range(7, 12, 2)]
            fast_list = [i for i in range(3, 6, 1)]
            aback_list = [i for i in range(5, 15, 2)]
            bback_list = [i for i in range(5, 15, 2)]
            fatr_list =  [i for i in np.arange(0.3, 0.8, 0.2)]
            for slow in slow_list:
                for fast in fast_list:
                    strategies.append(StartWithAwesomeOscillator(ohlcv
                                                                 , slow
                                                                 , fast
                                                                 , self.params["default"][2]
                                                                 , self.params["default"][3]
                                                                 , self.params["default"][4]))
            for aback in aback_list:
                for bback in bback_list:
                    for fatr in fatr_list:
                        strategies.append(StartWithAwesomeOscillator(ohlcv
                                                                     , self.params["default"][0]
                                                                     , self.params["default"][1]
                                                                     , aback
                                                                     , bback
                                                                     , fatr))
        return strategies


class StartWithAwesomeOscillator(EntryStrategy):
    """
    START WITH AWESOME OSCILLATOR
    """

    def __init__(self
                 , ohlcv
                 , fast_period
                 , slow_period
                 , aback
                 , bback
                 , fatr
                 , order_vol_ratio=0.01):
        self.title = f"StartAwesome[{slow_period:.0f},{fast_period:.0f},{aback:.0f},{bback:.0f},{fatr:.1f}]"
        self.ohlcv = ohlcv
        self.symbol = self.ohlcv.symbol
        self.ao = AwesomeOscillator(ohlcv, fast_period, slow_period)
        self.aback = aback
        self.bback = bback
        self.fatr = fatr
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.ao.ao[idx] == 0
        ):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        """
//bearish divergence
Condition2=AO[aback]<AO[bback];
condition3=low<low[1] and (close-low)/(high-low+.000001)>fatr;
if condition2 and condition3 then buy next bar at market;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.ao.slow_period:
            return OrderType.NONE_ORDER
        close0 = self.ohlcv.values['close'][idx]
        high0 = self.ohlcv.values['high'][idx]
        low0 = self.ohlcv.values['low'][idx]
        low1 = self.ohlcv.values['low'][idx - 1]
        condition2 = self.ao.ao[idx - self.aback] < self.ao.ao[idx - self.bback]
        condition3 = low0 > low1 and (close0 - low0) / (high0 - low0 + 0.000001) > self.fatr
        if condition2 and condition3:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
//Bullish divergence
Condition1=AO[aback]>AO[bback];
//bearish divergence
condition4=high>high[1] and (close-low)/(high-low+.000001)<(1-fatr);
if condition1 and condition4 then sellshort next bar at market;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.ao.slow_period:
            return OrderType.NONE_ORDER
        close0 = self.ohlcv.values['close'][idx]
        high0 = self.ohlcv.values['high'][idx]
        high1 = self.ohlcv.values['high'][idx - 1]
        low0 = self.ohlcv.values['low'][idx]
        condition1 = self.ao.ao[idx - self.aback] > self.ao.ao[idx - self.bback]
        condition4 = high0 > high1 and (close0 - low0) / (high0 - low0 + 0.000001) < (1 - self.fatr)
        if condition1 and condition4:
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
        ind1 = self.ao.ao[idx]
        ind2 = None
        ind3 = None
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class StartWithAwesomeOscillatorFactory(EntryStrategyFactory):
    params = {
        # atr_span, atr_mult, trima_span, lookback_span
        "default": [15, 0.5, 10, 10]
    }

    rough_params = [
        [15, 0.5, 10, 10]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            ao = self.params[s][0]
            aback = self.params[s][0]
            bback = self.params[s][0]
            fatr = self.params[s][0]
        else:
            ao = self.params["default"][0]
            aback = self.params["default"][1]
            bback = self.params["default"][2]
            fatr = self.params["default"][3]
        return StartWithAwesomeOscillator(ohlcv, atr_span, atr_mult, trima_span, lookback_span)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            for p in self.rough_params:
                strategies.append(StartWithAwesomeOscillator(ohlcv
                                                   , p[0]
                                                   , p[1]
                                                   , p[2]
                                                   , p[3]))
        else:
            atr_spans = [i for i in range(5, 25, 5)]
            atr_mults = [i for i in np.arange(0.3, 1.5, 0.2)]
            trima_spans = [i for i in range(5, 25, 5)]
            lookback_spans = [i for i in np.arange(5, 16, 5)]
            for atr_span in atr_spans:
                for atr_mult in atr_mults:
                    for trima_span in trima_spans:
                        for lookback_span in lookback_spans:
                            strategies.append(StartWithAwesomeOscillator(ohlcv, atr_span, atr_mult, trima_span, lookback_span))
        return strategies


class StartWithAwesomeOscillator(EntryStrategy):
    """
    START WITH AWESOME OSCILLATOR
    """
    def __init__(self
                 , title
                 , ohlcv
                 , ao
                 , aback
                 , bback
                 , fatr
                 , order_vol_ratio=0.01):
        self.title = title
        self.ohlcv = ohlcv
        self.symbol = self.ohlcv.symbol
        self.ao = ao
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
        low1 = self.ohlcv.values['low'][idx-1]
        condition2 = self.ao.ao[idx-self.aback] < self.ao.ao[idx-self.bback]
        condition3 = low0 > low1 and (close0-low0)/(high0-low0+0.000001) > self.fatr
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
        high1 = self.ohlcv.values['high'][idx-1]
        low0 = self.ohlcv.values['low'][idx]
        condition1 = self.ao.ao[idx-self.aback] > self.ao.ao[idx-self.bback]
        condition4 = high0 > high1 and (close0-low0)/(high0-low0+0.000001) < (1-self.fatr)
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

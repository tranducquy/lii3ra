from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.exponentially_smoothed_movingaverage import ExponentiallySmoothedMovingAverage
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy
from lii3ra.tick import Tick


class ExponentiallyBetterFactory(EntryStrategyFactory):
    params = {
        # fast_ema_span, slow_ema_span
        "default": [10, 20]
    }

    def create(self, ohlcv, optimization=False):
        strategies = []
        if not optimization:
            #
            s = ohlcv.symbol
            if s in self.params:
                fast_ema_span = self.params[s][0]
                slow_ema_span = self.params[s][1]
            else:
                fast_ema_span = self.params["default"][0]
                slow_ema_span = self.params["default"][1]
            strategies.append(ExponentiallyBetter(ohlcv, fast_ema_span, slow_ema_span))
        else:
            fast_spans = [i for i in range(3, 20, 3)]
            slow_spans = [i for i in range(10, 40, 3)]
            for fast_span in fast_spans:
                for slow_span in slow_spans:
                    strategies.append(ExponentiallyBetter(ohlcv, fast_span, slow_span))
        return strategies


class ExponentiallyBetter(EntryStrategy):
    """
    終値の指数移動平均がクロスしたらエントリー
    """

    def __init__(self
                 , ohlcv
                 , fast_ema_span
                 , slow_ema_span
                 , order_vol_ratio=0.01):
        self.title = f"ExponentiallyBetter[{fast_ema_span:.0f},{slow_ema_span:.0f}]"
        self.ohlcv = ohlcv
        self.fast_ema = ExponentiallySmoothedMovingAverage(ohlcv, fast_ema_span)
        self.slow_ema = ExponentiallySmoothedMovingAverage(ohlcv, slow_ema_span)
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio
        self.tick = Tick.get_tick(self.symbol)

    def _is_indicator_valid(self, idx):
        if (
                self.fast_ema.ema[idx] == 0
                or self.slow_ema.ema[idx] == 0):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        """
        終値の指数移動平均がクロスしたら逆指値でロング
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= 2:
            return OrderType.NONE_ORDER
        before_condition = self.fast_ema.ema[idx - 1] < self.slow_ema.ema[idx - 1]
        current_condition = self.fast_ema.ema[idx] > self.slow_ema.ema[idx]
        if before_condition and current_condition:
            return OrderType.STOP_MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        終値の指数移動平均がクロスしたら逆指値でショート
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= 2:
            return OrderType.NONE_ORDER
        before_condition = self.fast_ema.ema[idx - 1] > self.slow_ema.ema[idx - 1]
        current_condition = self.fast_ema.ema[idx] < self.slow_ema.ema[idx]
        if before_condition and current_condition:
            return OrderType.STOP_MARKET_SHORT
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
        ind1 = self.fast_ema.ema[idx]
        ind2 = self.slow_ema.ema[idx]
        ind3 = None
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

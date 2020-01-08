from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.relative_strength_index import RelativeStrengthIndex
from lii3ra.technical_indicator.exponentially_smoothed_movingaverage import ExponentiallySmoothedMovingAverage
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class RSITriggerFactory(EntryStrategyFactory):
    params = {
        # rsi_span, rsi_threshold, ema_span
        "default": [5, 80, 5]
        , "1570.T": [15, 60, 5]
    }

    rough_params = [
        [5, 80, 5]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            rsi_span = self.params[s][0]
            rsi_threshold = self.params[s][1]
            ema_span = self.params[s][2]
        else:
            rsi_span = self.params["default"][0]
            rsi_threshold = self.params["default"][1]
            ema_span = self.params["default"][2]
        return RSITrigger(ohlcv, rsi_span, rsi_threshold, ema_span)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            for p in self.rough_params:
                strategies.append(RSITrigger(ohlcv
                                             , p[0]
                                             , p[1]
                                             , p[2]))
        else:
            rsi_spans = [i for i in range(3, 16, 3)]
            rsi_thresholds = [i for i in range(20, 90, 10)]
            ema_spans = [i for i in range(5, 26, 5)]
            for rsi_span in rsi_spans:
                for rsi_threshold in rsi_thresholds:
                    for ema_span in ema_spans:
                        strategies.append(RSITrigger(ohlcv, rsi_span, rsi_threshold, ema_span))
        return strategies


class RSITrigger(EntryStrategy):
    """
    RSIがRSI Thresholdを下回っていて、終値が終値のEMAを下回っている場合、次のバーでロングを成行注文する
    RSIが100-RSI Thresholdを上回っていて、終値が終値のEMAを上回っている場合、次のバーでショートを成行注文する
    """

    def __init__(self
                 , ohlcv
                 , rsi_span
                 , rsi_threshold
                 , ema_span
                 , order_vol_ratio=0.01):
        self.title = f"RSITrigger[{rsi_span:.0f},{rsi_threshold:.0f},{ema_span:.0f}]"
        self.ohlcv = ohlcv
        self.symbol = self.ohlcv.symbol
        self.rsi = RelativeStrengthIndex(ohlcv, rsi_span)
        self.rsi_threshold = rsi_threshold
        self.ema = ExponentiallySmoothedMovingAverage(ohlcv, ema_span)
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

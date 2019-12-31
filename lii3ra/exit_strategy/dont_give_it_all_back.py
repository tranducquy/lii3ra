from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.average_true_range import AverageTrueRange
from lii3ra.exit_strategy.exit_strategy import ExitStrategyFactory
from lii3ra.exit_strategy.exit_strategy import ExitStrategy


class DontGiveItAllBackFactory(ExitStrategyFactory):
    params = {
        # long_atr_span, long_xatr, short_atr_span, short_xatr
        "default": [3, 0.20, 3, 0.20]
    }

    rough_params = [
        [3, 0.20, 3, 0.20]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            long_atr_span = self.params[s][0]
            long_xatr = self.params[s][1]
            short_atr_span = self.params[s][2]
            short_xatr = self.params[s][3]
        else:
            long_atr_span = self.params["default"][0]
            long_xatr = self.params["default"][1]
            short_atr_span = self.params["default"][2]
            short_xatr = self.params["default"][3]
        return DontGiveItAllBack(ohlcv
                                 , long_atr_span
                                 , long_xatr
                                 , short_atr_span
                                 , short_xatr)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            #
            for p in self.rough_params:
                strategies.append(DontGiveItAllBack(ohlcv, p[0], p[1], p[2], p[3]))
        else:
            long_atr_span_list = [i for i in range(3, 16, 3)]
            long_xatr_list = [0.05, 0.10, 0.20, 0.30]
            short_atr_span_list = [i for i in range(3, 16, 3)]
            short_xatr_list = [0.05, 0.10, 0.20, 0.30]
            for long_atr_span in long_atr_span_list:
                for long_xatr in long_xatr_list:
                    strategies.append(DontGiveItAllBack(ohlcv
                                                        , long_atr_span
                                                        , long_xatr
                                                        , self.params["default"][2]
                                                        , self.params["default"][3]))
            for short_atr_span in short_atr_span_list:
                for short_xatr in short_xatr_list:
                    strategies.append(DontGiveItAllBack(ohlcv
                                                        , self.params["default"][0]
                                                        , self.params["default"][1]
                                                        , short_atr_span
                                                        , short_xatr))
        return strategies


class DontGiveItAllBack(ExitStrategy):
    """
    最大含み益と現在の含み益の差がxATR*ATRよりも大きい場合、次のバーで成行でクローズする。
    """

    def __init__(self
                 , ohlcv
                 , long_atr_span=3
                 , long_xatr=0.2
                 , short_atr_span=3
                 , short_xatr=0.2):
        self.title = f"DontGiveItAllBack[{long_atr_span:.0f},{long_xatr:.2f}][{short_atr_span:.0f},{short_xatr:.2f}]"
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol
        self.long_atr = AverageTrueRange(ohlcv, long_atr_span)
        self.short_atr = AverageTrueRange(ohlcv, short_atr_span)
        self.long_xatr = long_xatr
        self.short_xatr = short_xatr
        self.max_profit = 0
        self.current_profit = None
        self.profit_diff = None

    def check_exit_long(self, pos_price, pos_vol, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx == entry_idx:
            self.current_profit = 0
            self.max_profit = 0
        close = self.ohlcv.values['close'][idx]
        self.current_profit = close - pos_price
        self.max_profit = self.current_profit if self.max_profit < self.current_profit else self.max_profit
        self.profit_diff = self.max_profit - self.current_profit
        if self.profit_diff > self.long_atr.atr[idx] * self.long_xatr:
            return OrderType.CLOSE_LONG_MARKET
        else:
            return OrderType.NONE_ORDER

    def check_exit_short(self, pos_price, pos_vol, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx == entry_idx:
            self.current_profit = 0
            self.max_profit = 0
        close = self.ohlcv.values['close'][idx]
        self.current_profit = pos_price - close
        self.max_profit = self.current_profit if self.max_profit < self.current_profit else self.max_profit
        self.profit_diff = self.max_profit - self.current_profit
        if self.profit_diff > self.short_atr.atr[idx] * self.short_xatr:
            return OrderType.CLOSE_SHORT_MARKET
        else:
            return OrderType.NONE_ORDER

    def create_order_exit_long_stop_market(self, idx, entry_idx):
        if not self._is_valid(idx):
            return 0.00
        # dummy
        price = self.ohlcv.values['close'][idx]
        return price

    def create_order_exit_short_stop_market(self, idx, entry_idx):
        if not self._is_valid(idx):
            return 0.00
        # dummy
        price = self.ohlcv.values['close'][idx]
        return price

    def create_order_exit_long_market(self, idx, entry_idx):
        return 0.00

    def create_order_exit_short_market(self, idx, entry_idx):
        return 0.00

    def get_indicators(self, idx, entry_idx):
        ind1 = self.long_atr.atr[idx]
        ind2 = (self.long_atr.atr[idx] * self.long_xatr)
        ind3 = self.short_atr.atr[idx]
        ind4 = (self.short_atr.atr[idx] * self.short_xatr)
        ind5 = self.max_profit if hasattr(self, "max_profit") else None
        ind6 = self.current_profit if hasattr(self, "current_profit") else None
        ind7 = self.profit_diff if hasattr(self, "profit_diff") else None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

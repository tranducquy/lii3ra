from lii3ra.ordertype import OrderType
from lii3ra.exit_strategy.exit_strategy import ExitStrategyFactory
from lii3ra.exit_strategy.exit_strategy import ExitStrategy


class TimedFactory(ExitStrategyFactory):
    params = {
        # long_bb_span, long_bb_ratio, short_bb_span, short_bb_ratio
        "default": [1, 3, 3, 0.03]
        , "^N225": [1, 3, 3, 0.03]
        , "6753.T": [1, 3, 1, 0.05]
        , "4043.T": [1, 3, 1, 0.03]
        , "5706.T": [1, 3, 1, 0.06]
        , "6704.T": [1, 3, 3, 0.03]
    }

    rough_params = [
        # long_bb_span, long_bb_ratio, short_bb_span, short_bb_ratio
        [1, 3, 3, 0.03]
        , [2, 3, 3, 0.03]
        , [1, 5, 5, 0.03]
        , [2, 5, 5, 0.03]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            imethod = self.params[s][0]
            long_span = self.params[s][1]
            short_span = self.params[s][2]
            losscut_ratio = self.params[s][3]
        else:
            imethod = self.params["default"][0]
            long_span = self.params["default"][1]
            short_span = self.params["default"][2]
            losscut_ratio = self.params["default"][3]
        return Timed(ohlcv, imethod, long_span, short_span, losscut_ratio)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            for p in self.rough_params:
                strategies.append(Timed(ohlcv, p[0], p[1], p[2], p[3]))
        else:
            imethods = [1, 2, 3]
            long_spans = [i for i in range(1, 5, 1)]
            short_spans = [i for i in range(1, 5, 1)]
            losscut_ratios = [0.03, 0.06]
            for imethod in imethods:
                for long_span in long_spans:
                    for short_span in short_spans:
                        for losscut_ratio in losscut_ratios:
                            strategies.append(Timed(ohlcv, imethod, long_span, short_span, losscut_ratio))
        return strategies


class Timed(ExitStrategy):
    """
    指定したバーが経過したら成行返済する。
    Entryした次のバーで返済する場合はnum_of_barsに1を設定する。
    """
    def __init__(self, ohlcv, imethod=1, num_of_bars_long=3, num_of_bars_short=3, losscut_ratio=0.03):
        self.title = f"Timed[{imethod}][{num_of_bars_long:.0f}]" \
                     f"[{num_of_bars_short:.0f}][{losscut_ratio:.2f}]"
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol
        self.imethod = imethod
        self.num_of_bars_long = num_of_bars_long
        self.num_of_bars_short = num_of_bars_short
        self.losscut_ratio = losscut_ratio

    def check_exit_long(self, pos_price, pos_vol, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        # exit after specified number of bars
        if self.imethod == 1:
            if idx >= entry_idx + self.num_of_bars_long - 1:
                return OrderType.CLOSE_LONG_MARKET
        # exit after specified number of bars, ONLY if position is currently porofitable
        elif self.imethod == 2:
            if (idx >= entry_idx + self.num_of_bars_long - 1
                    and pos_price < self.ohlcv.values['close'][idx]):
                return OrderType.CLOSE_LONG_MARKET
        # exit after specified number of bars, ONLY if position is currently losing
        elif self.imethod == 3:
            if (idx >= entry_idx + self.num_of_bars_long - 1
                    and pos_price > self.ohlcv.values['close'][idx]):
                return OrderType.CLOSE_LONG_MARKET
        # ロスカット
        close = self.ohlcv.values['close'][idx]
        losscut_price = pos_price - (pos_price * self.losscut_ratio)
        if close < losscut_price:
            return OrderType.CLOSE_LONG_MARKET
        else:
            return OrderType.NONE_ORDER

    def check_exit_short(self, pos_price, pos_vol, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        # exit after specified number of bars
        if self.imethod == 1:
            if idx >= entry_idx + self.num_of_bars_short - 1:
                return OrderType.CLOSE_SHORT_MARKET
        # exit after specified number of bars, ONLY if position is currently porofitable
        elif self.imethod == 2:
            if (idx >= entry_idx + self.num_of_bars_short - 1
                    and pos_price > self.ohlcv.values['close'][idx]):
                return OrderType.CLOSE_SHORT_MARKET
        # exit after specified number of bars, ONLY if position is currently losing
        elif self.imethod == 3:
            if (idx >= entry_idx + self.num_of_bars_short - 1
                    and pos_price < self.ohlcv.values['close'][idx]):
                return OrderType.CLOSE_SHORT_MARKET
        # ロスカット
        close = self.ohlcv.values['close'][idx]
        losscut_price = pos_price + (pos_price * self.losscut_ratio)
        if close > losscut_price:
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

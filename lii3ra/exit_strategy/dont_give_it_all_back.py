from lii3ra.ordertype import OrderType
from lii3ra.exit_strategy.exit_strategy import ExitStrategyFactory
from lii3ra.exit_strategy.exit_strategy import ExitStrategy


class DontGiveItAllBackFactory(ExitStrategyFactory):
    params = {
        # num_of_bars_long, num_of_bars_short, losscut_ratio
        "default": [3, 3, 0.05]
    }

    rough_params = [
        [3, 3, 0.05]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            num_of_bars_long = self.params[s][0]
            num_of_bars_short = self.params[s][1]
            losscut_ratio = self.params[s][2]
        else:
            num_of_bars_long = self.params["default"][0]
            num_of_bars_short = self.params["default"][1]
            losscut_ratio = self.params["default"][2]
        return GettingIsGood(ohlcv
                             , num_of_bars_long
                             , num_of_bars_short
                             , losscut_ratio)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            #
            for p in self.rough_params:
                strategies.append(GettingIsGood(ohlcv, p[0], p[1], p[2]))
        else:
            num_of_bars_list = [i for i in range(1, 5)]
            losscut_ratio_list = [0.03, 0.05, 0.10]
            for long_bars in num_of_bars_list:
                for short_bars in num_of_bars_list:
                    for losscut_ratio in losscut_ratio_list:
                        strategies.append(GettingIsGood(ohlcv
                                                        , long_bars
                                                        , short_bars
                                                        , losscut_ratio))
        return strategies


class DontGiveItAllBack(ExitStrategy):
    """
    最大含み益と現在の含み益の差がxATR*ATRよりも大きい場合、次のバーで成行でクローズする。
    """
    def __init__(self, title, ohlcv, long_atr, short_atr, long_xatr=0.2, short_xatr=0.2):
        self.title = title
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol
        self.long_atr = long_atr
        self.short_atr = short_atr
        self.long_xatr = long_xatr
        self.short_xatr = short_xatr
        self.max_profit = 0
    
    def check_exit_long(self, pos_price, idx, entry_idx):
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

    def check_exit_short(self, pos_price, idx, entry_idx):
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
        #dummy
        price = self.ohlcv.values['close'][idx]
        return price

    def create_order_exit_short_stop_market(self, idx, entry_idx):
        if not self._is_valid(idx):
            return 0.00
        #dummy
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
        return (ind1, ind2, ind3, ind4, ind5, ind6, ind7)

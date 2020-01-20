from lii3ra.ordertype import OrderType
from lii3ra.exit_strategy.exit_strategy import ExitStrategyFactory
from lii3ra.exit_strategy.exit_strategy import ExitStrategy


class ProfitProtectorFactory(ExitStrategyFactory):
    params = {
        # long_profit_floor, long_pp_ratio, short_profit_floor, short_pp_ratio
        "default": [80000, 0.80, 80000, 0.80, 0.05]
    }

    def create(self, ohlcv, optimization=False):
        strategies = []
        if not optimization:
            #
            s = ohlcv.symbol
            if s in self.params:
                long_profit_floor = self.params[s][0]
                long_pp_ratio = self.params[s][1]
                short_profit_floor = self.params[s][2]
                short_pp_ratio = self.params[s][3]
                losscut_ratio = self.params[s][4]
            else:
                long_profit_floor = self.params["default"][0]
                long_pp_ratio = self.params["default"][1]
                short_profit_floor = self.params["default"][2]
                short_pp_ratio = self.params["default"][3]
                losscut_ratio = self.params["default"][4]
            strategies.append(ProfitProtector(ohlcv
                                              , long_profit_floor
                                              , long_pp_ratio
                                              , short_profit_floor
                                              , short_pp_ratio
                                              , losscut_ratio))
        else:
            long_profit_floor_list = [i for i in range(3, 16, 3)]
            long_pp_ratio_list = [0.05, 0.10, 0.20, 0.30]
            short_profit_floor_list = [i for i in range(3, 16, 3)]
            short_pp_ratio_list = [0.05, 0.10, 0.20, 0.30]
            for long_profit_floor in long_profit_floor_list:
                for long_pp_ratio in long_pp_ratio_list:
                    strategies.append(ProfitProtector(ohlcv
                                                      , long_profit_floor
                                                      , long_pp_ratio
                                                      , self.params["default"][2]
                                                      , self.params["default"][3]
                                                      , self.params["default"][4]))
            for short_profit_floor in short_profit_floor_list:
                for short_pp_ratio in short_pp_ratio_list:
                    strategies.append(ProfitProtector(ohlcv
                                                      , self.params["default"][0]
                                                      , self.params["default"][1]
                                                      , short_profit_floor
                                                      , short_pp_ratio
                                                      , self.params["default"][4]))
        return strategies


class ProfitProtector(ExitStrategy):
    """
    ポジションの最大利益がprofit_floorより大きい場合に、
    現在のポジションの利益を最大利益で割った値がpp_ratioより小さい場合、次のバーで成行返済する。
    """

    def __init__(self
                 , ohlcv
                 , long_profit_floor=100000
                 , long_pp_ratio=0.6
                 , short_profit_floor=100000
                 , short_pp_ratio=0.6
                 , losscut_ratio=0.03):
        self.title = f"ProfitProtector[{long_profit_floor:.2f},{long_pp_ratio:.2f}]" \
                     f"[{short_profit_floor:.2f},{short_pp_ratio:.2f}][{losscut_ratio:.2f}]"
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol
        self.long_profit_floor = long_profit_floor
        self.long_pp_ratio = long_pp_ratio
        self.short_profit_floor = short_profit_floor
        self.short_pp_ratio = short_pp_ratio
        self.max_profit = 0
        self.current_profit = 0
        self.losscut_ratio = losscut_ratio

    def check_exit_long(self, pos_price, pos_vol, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx == entry_idx:
            self.current_profit = 0
            self.max_profit = 0
        close = self.ohlcv.values['close'][idx]
        self.current_profit = (close - pos_price) * pos_vol
        self.max_profit = self.current_profit if self.max_profit < self.current_profit else self.max_profit
        if self.max_profit >= self.long_profit_floor:
            if (self.current_profit / self.max_profit) < self.long_pp_ratio:
                return OrderType.CLOSE_LONG_MARKET
        # 最低losscut設定
        losscut_price = pos_price - (pos_price * self.losscut_ratio)
        if close < losscut_price:
            return OrderType.CLOSE_LONG_MARKET
        return OrderType.NONE_ORDER

    def check_exit_short(self, pos_price, pos_vol, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx == entry_idx:
            self.current_profit = 0
            self.max_profit = 0
        close = self.ohlcv.values['close'][idx]
        self.current_profit = (pos_price - close) * pos_vol
        self.max_profit = self.current_profit if self.max_profit < self.current_profit else self.max_profit
        if self.max_profit >= self.short_profit_floor:
            if (self.current_profit / self.max_profit) < self.short_pp_ratio:
                return OrderType.CLOSE_SHORT_MARKET
        # 最低losscut設定
        losscut_price = pos_price + (pos_price * self.losscut_ratio)
        if close > losscut_price:
            return OrderType.CLOSE_SHORT_MARKET
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
        ind1 = self.max_profit
        ind2 = self.current_profit
        ind3 = (self.current_profit / self.max_profit) if self.current_profit != 0 and self.max_profit != 0 else None
        ind4 = self.long_profit_floor
        ind5 = self.long_pp_ratio
        ind6 = self.short_profit_floor
        ind7 = self.short_pp_ratio
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

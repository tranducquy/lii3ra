from lii3ra.ordertype import OrderType
from lii3ra.exit_strategy.exit_strategy import ExitStrategyFactory
from lii3ra.exit_strategy.exit_strategy import ExitStrategy


class TieredFactory(ExitStrategyFactory):
    # TODO:ATR

    params = {
        # long_profit_floor1, long_profit_floor2, long_profit_floor3
        # long_profit_ratio1, long_profit_ratio2, long_profit_ratio3
        # short_profit_floor1, short_profit_floor2, short_profit_floor3
        # short_profit_ratio1, short_profit_ratio2, short_profit_ratio3
        "default": [30000, 50000, 100000, 0.60, 0.75, 0.90, 30000, 50000, 100000, 0.60, 0.75, 0.90, 0.05]
    }

    def create(self, ohlcv, optimization=False):
        strategies = []
        if not optimization:
            #
            s = ohlcv.symbol
            if s in self.params:
                long_profit_floor1 = self.params[s][0]
                long_profit_floor2 = self.params[s][1]
                long_profit_floor3 = self.params[s][2]
                long_profit_ratio1 = self.params[s][3]
                long_profit_ratio2 = self.params[s][4]
                long_profit_ratio3 = self.params[s][5]
                short_profit_floor1 = self.params[s][6]
                short_profit_floor2 = self.params[s][7]
                short_profit_floor3 = self.params[s][8]
                short_profit_ratio1 = self.params[s][9]
                short_profit_ratio2 = self.params[s][10]
                short_profit_ratio3 = self.params[s][11]
                losscut_ratio = self.params[s][12]
            else:
                long_profit_floor1 = self.params["default"][0]
                long_profit_floor2 = self.params["default"][1]
                long_profit_floor3 = self.params["default"][2]
                long_profit_ratio1 = self.params["default"][3]
                long_profit_ratio2 = self.params["default"][4]
                long_profit_ratio3 = self.params["default"][5]
                short_profit_floor1 = self.params["default"][6]
                short_profit_floor2 = self.params["default"][7]
                short_profit_floor3 = self.params["default"][8]
                short_profit_ratio1 = self.params["default"][9]
                short_profit_ratio2 = self.params["default"][10]
                short_profit_ratio3 = self.params["default"][11]
                losscut_ratio = self.params["default"][12]
            strategies.append(Tiered(ohlcv
                                     , long_profit_floor1, long_profit_floor2, long_profit_floor3
                                     , long_profit_ratio1, long_profit_ratio2, long_profit_ratio3
                                     , short_profit_floor1, short_profit_floor2, short_profit_floor3
                                     , short_profit_ratio1, short_profit_ratio2, short_profit_ratio3
                                     , losscut_ratio))
        else:
            profit_floor1_list = [10000, 30000, 50000, 100000]
            profit_floor2_list = [30000, 50000, 100000, 200000]
            profit_floor3_list = [50000, 100000, 150000, 300000]
            profit_ratio1_list = [0.50, 0.60, 0.70]
            profit_ratio2_list = [0.60, 0.70, 0.80]
            profit_ratio3_list = [0.70, 0.80, 0.90]
            for profit_floor1 in profit_floor1_list:
                for profit_ratio1 in profit_ratio1_list:
                    for profit_floor2 in profit_floor2_list:
                        for profit_ratio2 in profit_ratio2_list:
                            for profit_floor3 in profit_floor3_list:
                                for profit_ratio3 in profit_ratio3_list:
                                    strategies.append(Tiered(ohlcv
                                                             , profit_floor1
                                                             , profit_floor2
                                                             , profit_floor3
                                                             , profit_ratio1
                                                             , profit_ratio2
                                                             , profit_ratio3
                                                             , self.params["default"][6]
                                                             , self.params["default"][7]
                                                             , self.params["default"][8]
                                                             , self.params["default"][9]
                                                             , self.params["default"][10]
                                                             , self.params["default"][11]
                                                             , self.params["default"][12]
                                                             ))
            for profit_floor1 in profit_floor1_list:
                for profit_ratio1 in profit_ratio1_list:
                    for profit_floor2 in profit_floor2_list:
                        for profit_ratio2 in profit_ratio2_list:
                            for profit_floor3 in profit_floor3_list:
                                for profit_ratio3 in profit_ratio3_list:
                                    strategies.append(Tiered(ohlcv
                                                             , self.params["default"][0]
                                                             , self.params["default"][1]
                                                             , self.params["default"][2]
                                                             , self.params["default"][3]
                                                             , self.params["default"][4]
                                                             , self.params["default"][5]
                                                             , profit_floor1
                                                             , profit_floor2
                                                             , profit_floor3
                                                             , profit_ratio1
                                                             , profit_ratio2
                                                             , profit_ratio3
                                                             , self.params["default"][12]
                                                             ))
        return strategies


class Tiered(ExitStrategy):
    """
    ポジションの最大利益がprofit_floorより大きい場合に、
    現在のポジションの利益を最大利益で割った値がprofit_ratioより小さい場合、次のバーで成行返済する。
    profit_floorを三段階用意する。
    """

    def __init__(self
                 , ohlcv
                 , long_profit_floor1
                 , long_profit_floor2
                 , long_profit_floor3
                 , long_profit_ratio1
                 , long_profit_ratio2
                 , long_profit_ratio3
                 , short_profit_floor1
                 , short_profit_floor2
                 , short_profit_floor3
                 , short_profit_ratio1
                 , short_profit_ratio2
                 , short_profit_ratio3
                 , losscut_ratio
                 ):
        self.title = f"Tiered[{long_profit_floor1:.0f},{long_profit_floor2:.0f},{long_profit_floor3:.0f}" \
                     f",{long_profit_ratio1:.2f},{long_profit_ratio2:.2f},{long_profit_ratio3:.2f}]" \
                     f"[{short_profit_floor1:.2f},{short_profit_floor2:.2f},{short_profit_floor3:.2f}" \
                     f",{short_profit_ratio1:.2f},{short_profit_ratio2:.2f},{short_profit_ratio3:.2f}]"
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol
        self.long_profit_floor1 = long_profit_floor1
        self.long_profit_ratio1 = long_profit_ratio1
        self.long_profit_floor2 = long_profit_floor2
        self.long_profit_ratio2 = long_profit_ratio2
        self.long_profit_floor3 = long_profit_floor3
        self.long_profit_ratio3 = long_profit_ratio3
        self.short_profit_floor1 = short_profit_floor1
        self.short_profit_ratio1 = short_profit_ratio1
        self.short_profit_floor2 = short_profit_floor2
        self.short_profit_ratio2 = short_profit_ratio2
        self.short_profit_floor3 = short_profit_floor3
        self.short_profit_ratio3 = short_profit_ratio3
        self.losscut_ratio = losscut_ratio
        self.max_profit = 0
        self.profit_ratio = 0

    def check_exit_long(self, pos_price, pos_vol, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx == entry_idx:
            self.current_profit = 0
            self.max_profit = 0
        close = self.ohlcv.values['close'][idx]
        self.current_profit = (close - pos_price) * pos_vol
        self.max_profit = self.current_profit if self.max_profit < self.current_profit else self.max_profit
        self.profit_ratio = 0
        if self.max_profit >= self.long_profit_floor1:
            self.profit_ratio = self.long_profit_ratio1
        if self.max_profit >= self.long_profit_floor2:
            self.profit_ratio = self.long_profit_ratio2
        if self.max_profit >= self.long_profit_floor3:
            self.profit_ratio = self.long_profit_ratio3
        if self.max_profit >= self.long_profit_floor1:
            if (self.current_profit / self.max_profit) <= self.profit_ratio:
                return OrderType.CLOSE_LONG_MARKET
        # 損切り
        losscut_price = pos_price - (pos_price * self.losscut_ratio)
        if close <= losscut_price:
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
        self.current_profit = (pos_price - close) * pos_vol
        self.max_profit = self.current_profit if self.max_profit < self.current_profit else self.max_profit
        self.profit_ratio = 0
        if self.max_profit >= self.short_profit_floor1:
            self.profit_ratio = self.short_profit_ratio1
        if self.max_profit >= self.short_profit_floor2:
            self.profit_ratio = self.short_profit_ratio2
        if self.max_profit >= self.short_profit_floor3:
            self.profit_ratio = self.short_profit_ratio3
        if self.max_profit >= self.short_profit_floor1:
            if (self.current_profit / self.max_profit) <= self.profit_ratio:
                return OrderType.CLOSE_SHORT_MARKET
        # 損切り
        losscut_price = pos_price + (pos_price * self.losscut_ratio)
        if close >= losscut_price:
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
        ind1 = self.max_profit
        ind2 = self.current_profit if hasattr(self, "current_profit") else None
        ind3 = (self.current_profit / self.max_profit) if self.max_profit != 0 and hasattr(self,
                                                                                           "current_profit") else None
        ind4 = self.profit_ratio
        ind5 = None  # TODO:損切りライン
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

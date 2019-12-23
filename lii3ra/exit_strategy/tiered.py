from lii3ra.ordertype import OrderType
from lii3ra.exit_strategy.exit_strategy import ExitStrategy


class Tiered(ExitStrategy):
    """
    ポジションの最大利益がprofit_floorより大きい場合に、
    現在のポジションの利益を最大利益で割った値がpp_ratioより小さい場合、次のバーで成行返済する。
    profit_floorを三段階用意する。
    """

    def __init__(self, title, ohlcv
                 , long_profit_floor1
                 , long_pp_ratio1
                 , long_profit_floor2
                 , long_pp_ratio2
                 , long_profit_floor3
                 , long_pp_ratio3
                 , short_profit_floor1
                 , short_pp_ratio1
                 , short_profit_floor2
                 , short_pp_ratio2
                 , short_profit_floor3
                 , short_pp_ratio3
                 , losscut_ratio
                 ):
        self.title = title
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol
        self.long_profit_floor1 = long_profit_floor1
        self.long_pp_ratio1 = long_pp_ratio1
        self.long_profit_floor2 = long_profit_floor2
        self.long_pp_ratio2 = long_pp_ratio2
        self.long_profit_floor3 = long_profit_floor3
        self.long_pp_ratio3 = long_pp_ratio3
        self.short_profit_floor1 = short_profit_floor1
        self.short_pp_ratio1 = short_pp_ratio1
        self.short_profit_floor2 = short_profit_floor2
        self.short_pp_ratio2 = short_pp_ratio2
        self.short_profit_floor3 = short_profit_floor3
        self.short_pp_ratio3 = short_pp_ratio3
        self.losscut_ratio = losscut_ratio
        self.max_profit = 0
        self.pp_ratio = 0

    def check_exit_long(self, pos_price, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx == entry_idx:
            self.current_profit = 0
            self.max_profit = 0
        close = self.ohlcv.values['close'][idx]
        self.current_profit = close - pos_price
        self.max_profit = self.current_profit if self.max_profit < self.current_profit else self.max_profit
        self.pp_ratio = 0
        if self.max_profit >= self.long_profit_floor1:
            self.pp_ratio = self.long_pp_ratio1
        if self.max_profit >= self.long_profit_floor2:
            self.pp_ratio = self.long_pp_ratio2
        if self.max_profit >= self.long_profit_floor3:
            self.pp_ratio = self.long_pp_ratio3
        if self.max_profit >= self.long_profit_floor1:
            if (self.current_profit / self.max_profit) <= self.pp_ratio:
                return OrderType.CLOSE_LONG_MARKET
        # 損切り
        losscut_price = pos_price - (pos_price * self.losscut_ratio)
        if close <= losscut_price:
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
        self.pp_ratio = 0
        if self.max_profit >= self.short_profit_floor1:
            self.pp_ratio = self.short_pp_ratio1
        if self.max_profit >= self.short_profit_floor2:
            self.pp_ratio = self.short_pp_ratio2
        if self.max_profit >= self.short_profit_floor3:
            self.pp_ratio = self.short_pp_ratio3
        if self.max_profit >= self.short_profit_floor1:
            if (self.current_profit / self.max_profit) <= self.pp_ratio:
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
        ind4 = self.pp_ratio
        ind5 = None  # TODO:損切りライン
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

from lii3ra.ordertype import OrderType
from lii3ra.exit_strategy.exit_strategy import ExitStrategy


class ContractGainLoss(ExitStrategy):
    """
    終値が指定した利益率を超えている場合、成行でクローズする
    書籍ではpipsだが、ここではpercent
    """

    def __init__(self, title, ohlcv, imethod, profit_ratio, loss_ratio, atr=None, specified_profit_ratio=0,
                 specified_loss_ratio=0):
        self.title = title
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol
        self.imethod = imethod
        self.profit_ratio = profit_ratio
        self.loss_ratio = loss_ratio
        self.atr = atr
        self.specified_profit_ratio = specified_profit_ratio
        self.specified_loss_ratio = specified_loss_ratio
        self.profit_target = None
        self.loss_target = None

    def check_exit_long(self, pos_price, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        # used stops and profit targets.
        if self.imethod == 1:
            self.profit_target = pos_price + (pos_price * self.profit_ratio)
            self.loss_target = pos_price - (pos_price * self.loss_ratio)
        # used stops and targets based on the recent ATR, multiplied by profit_ratio or loss_ratio.
        elif self.imethod == 2 and self.atr is not None:
            self.profit_target = pos_price + (self.atr.atr[entry_idx] * self.profit_ratio)
            self.loss_target = pos_price - (self.atr.atr[entry_idx] * self.loss_ratio)
        # calculate using imethod.2, but include a check to make sure the stop does not go below some minimum value for the stop or the profit target.
        elif self.imethod == 3 and self.atr is not None:
            atr_profit_target = pos_price + (self.atr.atr[entry_idx] * self.profit_ratio)
            specified_profit_target = pos_price + (pos_price * self.specified_profit_ratio)
            self.profit_target = atr_profit_target if specified_profit_target > atr_profit_target else specified_profit_target
            atr_loss_target = pos_price - (self.atr.atr[entry_idx] * self.loss_ratio)
            specified_loss_target = pos_price - (self.atr.atr[entry_idx] * self.specified_loss_ratio)
            self.loss_target = atr_loss_target if specified_loss_target > atr_loss_target else specified_loss_target
        # calculate using imethod.2, but include a check to make sure the stop does not go above the specified maximum value for the stop or the profit target.
        elif self.imethod == 4 and self.atr is not None:
            atr_profit_target = pos_price + (self.atr.atr[entry_idx] * self.profit_ratio)
            specified_profit_target = pos_price + (pos_price * self.specified_profit_ratio)
            self.profit_target = atr_profit_target if specified_profit_target < atr_profit_target else specified_profit_target
            atr_loss_target = pos_price - (self.atr.atr[entry_idx] * self.loss_ratio)
            specified_loss_target = pos_price - (self.atr.atr[entry_idx] * self.specified_loss_ratio)
            self.loss_target = atr_loss_target if specified_loss_target < atr_loss_target else specified_loss_target
        else:
            return OrderType.NONE_ORDER
        if close < self.loss_target or close > self.profit_target:
            return OrderType.CLOSE_LONG_MARKET
        else:
            return OrderType.NONE_ORDER

    def check_exit_short(self, pos_price, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        close = self.ohlcv.values['close'][idx]
        # used stops and profit targets.
        if self.imethod == 1:
            self.profit_target = pos_price - (pos_price * self.profit_ratio)
            self.loss_target = pos_price + (pos_price * self.loss_ratio)
        # used stops and targets based on the recent ATR, multiplied by profit_ratio or loss_ratio.
        elif self.imethod == 2 and self.atr is not None:
            self.profit_target = pos_price - (self.atr.atr[entry_idx] * self.profit_ratio)
            self.loss_target = pos_price + (self.atr.atr[entry_idx] * self.loss_ratio)
        # calculate using imethod.2, but include a check to make sure the stop does not go below some minimum value for the stop or the profit target.
        elif self.imethod == 3 and self.atr is not None:
            atr_profit_target = pos_price - (self.atr.atr[entry_idx] * self.profit_ratio)
            specified_profit_target = pos_price - (pos_price * self.specified_profit_ratio)
            self.profit_target = atr_profit_target if specified_profit_target < atr_profit_target else specified_profit_target
            atr_loss_target = pos_price + (self.atr.atr[entry_idx] * self.loss_ratio)
            specified_loss_target = pos_price + (pos_price * self.specified_loss_ratio)
            self.loss_target = atr_loss_target if specified_loss_target < atr_loss_target else specified_loss_target
        # calculate using imethod.2, but include a check to make sure the stop does not go above the specified maximum value for the stop or the profit target.
        elif self.imethod == 4 and self.atr is not None:
            atr_profit_target = pos_price - (self.atr.atr[entry_idx] * self.profit_ratio)
            specified_profit_target = pos_price - (pos_price * self.specified_profit_ratio)
            self.profit_target = atr_profit_target if specified_profit_target > atr_profit_target else specified_profit_target
            atr_loss_target = pos_price + (self.atr.atr[entry_idx] * self.loss_ratio)
            specified_loss_target = pos_price + (pos_price * self.specified_loss_ratio)
            self.loss_target = atr_loss_target if specified_loss_target > atr_loss_target else specified_loss_target
        else:
            return OrderType.NONE_ORDER
        if close > self.loss_target or close < self.profit_target:
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
        ind1 = self.profit_target if hasattr(self, "profit_target") else None
        ind2 = self.loss_target if hasattr(self, "loss_target") else None
        ind3 = None
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

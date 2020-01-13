import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.average_true_range import AverageTrueRange
from lii3ra.exit_strategy.exit_strategy import ExitStrategyFactory
from lii3ra.exit_strategy.exit_strategy import ExitStrategy


class ContractGainLossFactory(ExitStrategyFactory):

    params = {
        # imethod, profit_ratio, loss_ratio, atr_span, specified_profit_ratio, specified_loss_ratio
        "default": [1, 0.06, 0.02, 14, 0.30, 0.10]
        # , "3038.T": [1, 0.09, 0.03, 14, 0.30, 0.10]
        , "3038.T": [2, 1.00, 0.10, 15, 0.06, 0.01]
        , "6920.T": [1, 0.09, 0.06, 14, 0.09, 0.03]
        , "9424.T": [4, 1.00, 0.30, 5, 0.06, 0.03]
        , "2412.T": [1, 0.06, 0.02, 14, 0.30, 0.10]
        , "4967.T": [1, 0.06, 0.02, 14, 0.30, 0.10]
        , "6473.T": [1, 0.06, 0.03, 14, 0.09, 0.03]
    }

    rough_params = [
        [1, 0.06, 0.02, 14, 0.30, 0.10]
        , [1, 0.09, 0.03, 14, 0.30, 0.10]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            imethod = self.params[s][0]
            profit_ratio = self.params[s][1]
            loss_ratio = self.params[s][2]
            atr_span = self.params[s][3]
            specified_profit_ratio = self.params[s][4]
            specified_loss_ratio = self.params[s][5]
        else:
            imethod = self.params["default"][0]
            profit_ratio = self.params["default"][1]
            loss_ratio = self.params["default"][2]
            atr_span = self.params["default"][3]
            specified_profit_ratio = self.params["default"][4]
            specified_loss_ratio = self.params["default"][5]
        return ContractGainLoss(ohlcv
                                , imethod
                                , profit_ratio
                                , loss_ratio
                                , atr_span
                                , specified_profit_ratio
                                , specified_loss_ratio)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            for p in self.rough_params:
                strategies.append(ContractGainLoss(ohlcv, p[0], p[1], p[2], p[3], p[4], p[5]))
        else:
            profit_ratio_list = [0.03, 0.06, 0.09]
            loss_ratio_list = [0.01, 0.03, 0.06]
            imethod = 1
            for profit_ratio in profit_ratio_list:
                for loss_ratio in loss_ratio_list:
                    if profit_ratio > loss_ratio:
                        strategies.append(ContractGainLoss(ohlcv
                                                           , imethod
                                                           , profit_ratio
                                                           , loss_ratio))
            imethod_list = [2, 3, 4]
            profit_ratio_list = [0.25, 0.50, 1.00]
            loss_ratio_list = [0.10, 0.30, 0.60]
            atr_span_list = [i for i in range(5, 20, 5)]
            specified_profit_ratio_list = [0.03, 0.06, 0.09]
            specified_loss_ratio_list = [0.01, 0.03, 0.06]
            for imethod in imethod_list:
                for profit_ratio in profit_ratio_list:
                    for loss_ratio in loss_ratio_list:
                        for atr_span in atr_span_list:
                            for specified_profit_ratio in specified_profit_ratio_list:
                                for specified_loss_ratio in specified_loss_ratio_list:
                                    if profit_ratio > loss_ratio:
                                        if specified_profit_ratio > specified_loss_ratio:
                                            strategies.append(ContractGainLoss(ohlcv
                                                                               , imethod
                                                                               , profit_ratio
                                                                               , loss_ratio
                                                                               , atr_span
                                                                               , specified_profit_ratio
                                                                               , specified_loss_ratio))
        return strategies


class ContractGainLoss(ExitStrategy):
    """
    終値が指定した利益率を超えている場合、Exit
     - 注文方法:寄成
    """

    def __init__(self
                 , ohlcv
                 , imethod
                 , profit_ratio
                 , loss_ratio
                 , atr_span=14
                 , specified_profit_ratio=0.09
                 , specified_loss_ratio=0.03):
        self.title = f"Contract[{imethod:.0f}][{profit_ratio:.2f},{loss_ratio:.2f}][{atr_span:.0f}]"\
                     f"[{specified_profit_ratio:.2f},{specified_loss_ratio:.2f}]"
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol
        self.imethod = imethod
        self.profit_ratio = profit_ratio
        self.loss_ratio = loss_ratio
        self.atr = AverageTrueRange(ohlcv, atr_span)
        self.specified_profit_ratio = specified_profit_ratio
        self.specified_loss_ratio = specified_loss_ratio
        self.profit_target = None
        self.loss_target = None

    def check_exit_long(self, pos_price, pos_vol, idx, entry_idx):
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
        # calculate using imethod.2, but include a check to make sure the stop does not go below some minimum value
        # for the stop or the profit target.
        elif self.imethod == 3 and self.atr is not None:
            atr_profit_target = pos_price + (self.atr.atr[entry_idx] * self.profit_ratio)
            specified_profit_target = pos_price + (pos_price * self.specified_profit_ratio)
            self.profit_target = atr_profit_target if specified_profit_target > atr_profit_target else specified_profit_target
            atr_loss_target = pos_price - (self.atr.atr[entry_idx] * self.loss_ratio)
            specified_loss_target = pos_price - (self.atr.atr[entry_idx] * self.specified_loss_ratio)
            self.loss_target = atr_loss_target if specified_loss_target > atr_loss_target else specified_loss_target
        # calculate using imethod.2, but include a check to make sure the stop does not go above the specified
        # maximum value for the stop or the profit target.
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

    def check_exit_short(self, pos_price, pos_vol, idx, entry_idx):
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
        # calculate using imethod.2, but include a check to make sure the stop does not go below some minimum value
        # for the stop or the profit target.
        elif self.imethod == 3 and self.atr is not None:
            atr_profit_target = pos_price - (self.atr.atr[entry_idx] * self.profit_ratio)
            specified_profit_target = pos_price - (pos_price * self.specified_profit_ratio)
            self.profit_target = atr_profit_target if specified_profit_target < atr_profit_target else specified_profit_target
            atr_loss_target = pos_price + (self.atr.atr[entry_idx] * self.loss_ratio)
            specified_loss_target = pos_price + (pos_price * self.specified_loss_ratio)
            self.loss_target = atr_loss_target if specified_loss_target < atr_loss_target else specified_loss_target
        # calculate using imethod.2, but include a check to make sure the stop does not go above the specified
        # maximum value for the stop or the profit target.
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
        ind3 = self.atr.atr[idx]
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

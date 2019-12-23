# -*- coding: utf-8 -*-

import math
from lii3ra.fee import Fee
from lii3ra.unit import Unit


class Asset:
    def __init__(self, symbol, initial_cash, leverage=3.0, losscut_ratio=0.10):
        self.symbol = symbol
        self.initial_cash = initial_cash
        self.before_cash = initial_cash
        self.cash = initial_cash
        self.leverage = leverage
        self.losscut_ratio = losscut_ratio
        self.unit = Unit.get_unit(symbol)
        self.last_fee = 0
        self.last_spread_fee = 0

    def get_losscut_ratio(self, symbol):
        return self.losscut_ratio

    def _calc_leverage(self, symbol, factor):
        # TODO:factor対応
        return self.leverage

    def get_margin_cash(self, symbol, factor=1):
        leverage = self._calc_leverage(symbol, factor)
        return math.floor(self.cash * leverage), leverage

    def get_max_vol(self, price, factor=1):
        # TODO:最小単元
        (margin_cash, _) = self.get_margin_cash(factor)
        return math.floor(margin_cash / price)

    def entry_long(self, price, vol):
        self.last_fee = 0
        self.last_spread_fee = 0
        self.before_cash = self.cash
        self.cash = round(self.cash - price * vol, 2)

    def entry_short(self, price, vol):
        self.last_fee = 0
        self.last_spread_fee = 0
        self.before_cash = self.cash
        self.cash = round(self.cash + price * (vol * -1), 2)

    def exit_long(self, price, vol):
        fee = abs(Fee.get_fee(self.symbol))
        fee_per_unit = abs(Fee.get_fee_per_unit(self.symbol))
        spread = Fee.get_spread(self.symbol)
        spread_fee = abs(spread * vol)
        self.last_fee = abs(fee) + abs(fee_per_unit * int(vol / self.unit))
        self.last_spread_fee = abs(spread_fee)
        self.cash = round(self.cash + (price * vol) - self.last_spread_fee - self.last_fee, 2)

    def exit_short(self, price, vol):
        fee = abs(Fee.get_fee(self.symbol))
        fee_per_unit = abs(Fee.get_fee_per_unit(self.symbol))
        spread = Fee.get_spread(self.symbol)
        spread_fee = abs(spread * vol)
        self.last_fee = abs(fee) + abs(fee_per_unit * int(vol / self.unit))
        self.last_spread_fee = spread_fee
        self.cash = round(self.cash + (price * vol) - self.last_spread_fee - self.last_fee, 2)

import math
import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.average_true_range import AverageTrueRange
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class AsymmetricAgainIntroSerialFactory(EntryStrategyFactory):
    params = {
        # atr_span, atr_mult
        "default": [15, 0.5, 5, 20]
        , "3038.T": [20, 0.3, 0, 0]
    }

    def create(self, ohlcv, optimization=False):
        strategies = []
        if not optimization:
            #
            s = ohlcv.symbol
            if s in self.params:
                atr_span = self.params[s][0]
                atr_mult = self.params[s][1]
                winner_wait_period = self.params[s][2]
                loser_wait_period = self.params[s][3]
            else:
                atr_span = self.params["default"][0]
                atr_mult = self.params["default"][1]
                winner_wait_period = self.params["default"][2]
                loser_wait_period = self.params["default"][3]
            strategies.append(AsymmetricAgainIntroSerial(ohlcv
                                                         , atr_span
                                                         , atr_mult
                                                         , winner_wait_period
                                                         , loser_wait_period))
        else:
            atr_spans = [i for i in range(5, 25, 5)]
            atr_mults = [i for i in np.arange(0.3, 1.5, 0.2)]
            winner_wait_period_list = [i for i in range(0, 15, 5)]
            loser_wait_period_list = [i for i in range(0, 15, 5)]
            for atr_span in atr_spans:
                for atr_mult in atr_mults:
                    for winner_wait_period in winner_wait_period_list:
                        for loser_wait_period in loser_wait_period_list:
                            strategies.append(AsymmetricAgainIntroSerial(ohlcv
                                                                         , atr_span
                                                                         , atr_mult
                                                                         , winner_wait_period
                                                                         , loser_wait_period))
        return strategies


class AsymmetricAgainIntroSerial(EntryStrategy):
    """
    前日安値でエントリーを判定し、ATRを用いて逆指値注文する
    """

    def __init__(self
                 , ohlcv
                 , atr_span
                 , atr_mult
                 , winner_wait_period
                 , loser_wait_period
                 , order_vol_ratio=0.01):
        self.title = f"AsymmetricAgainIntroSerial[{atr_span:.0f},{atr_mult:.2f}][{winner_wait_period:.0f},{loser_wait_period:.0f}]"
        self.ohlcv = ohlcv
        self.atr = AverageTrueRange(ohlcv, atr_span)
        self.atr_mult = atr_mult
        self.winner_wait_period = winner_wait_period
        self.loser_wait_period = loser_wait_period
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.atr.atr[idx] == 0
        ):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        """
        前日安値が当日始値よりも安い場合は逆指値でロングのエントリー
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.atr.atr_span:
            return OrderType.NONE_ORDER
        if len(self.position.exit_positions_profit) == 0:
            initial_trade = True
            last_exit_profit = 0
        else:
            initial_trade = False
            last_exit_profit = self.position.exit_positions_profit[-1]
        condition1 = initial_trade \
                     or (last_exit_profit > 0 and idx - last_exit_idx >= self.winner_wait_period) \
                     or (last_exit_profit <= 0 and idx - last_exit_idx >= self.loser_wait_period)
        value1 = self.ohlcv.values['open'][idx]
        value2 = self.ohlcv.values['low'][idx - 1]
        if not np.isnan(value1) and not np.isnan(value2) and (value1 >= value2 and condition1):
            return OrderType.STOP_MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        前日安値が当日始値よりも高い場合は逆指値でショートのエントリー
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.atr.atr_span:
            return OrderType.NONE_ORDER
        if len(self.position.exit_positions_profit) == 0:
            initial_trade = True
            last_exit_profit = 0
        else:
            initial_trade = False
            last_exit_profit = self.position.exit_positions_profit[-1]
        condition1 = initial_trade \
                     or (last_exit_profit > 0 and idx - last_exit_idx >= self.winner_wait_period) \
                     or (last_exit_profit <= 0 and idx - last_exit_idx >= self.loser_wait_period)
        value1 = self.ohlcv.values['open'][idx]
        value2 = self.ohlcv.values['low'][idx - 1]
        if np.isnan(value1) or np.isnan(value2) or (value1 >= value2 and condition1):
            return OrderType.NONE_ORDER
        else:
            # return OrderType.NONE_ORDER
            return OrderType.STOP_MARKET_SHORT

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
        close = self.ohlcv.values['close'][idx]
        price = math.ceil(close + self.atr_mult * self.atr.atr[idx])
        return price

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        low = self.ohlcv.values['low'][idx]
        price = math.floor(low - self.atr_mult * self.atr.atr[idx])
        return price

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
        ind1 = self.ohlcv.values['close'][idx] + self.atr.atr[idx] * self.atr_mult
        ind2 = self.ohlcv.values['low'][idx] - self.atr.atr[idx] * self.atr_mult
        ind3 = self.atr.atr[idx]
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

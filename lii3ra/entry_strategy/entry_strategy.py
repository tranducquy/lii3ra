import math
import numpy
from lii3ra.unit import Unit


class EntryStrategyFactory:

    def create(self, ohlcv, optimization):
        raise NotImplementedError


class EntryStrategy:
    """ポジションエントリー用のストラテジー"""

    def __init__(self, ohlcv, order_vol_ratio=0.01, ema=None):
        self.title = "EntryStrategy"
        self.ohlcv = ohlcv
        self.ema = ema
        self.symbol = ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio
        self.position = None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    def set_position(self, p):
        self.position = p

    def _is_valid(self, idx):
        if (
                self.ohlcv.values['open'][idx] is None
                or self.ohlcv.values['high'][idx] is None
                or self.ohlcv.values['low'][idx] is None
                or self.ohlcv.values['close'][idx] is None
                or numpy.isnan(self.ohlcv.values['open'][idx])
                or numpy.isnan(self.ohlcv.values['high'][idx])
                or numpy.isnan(self.ohlcv.values['low'][idx])
                or numpy.isnan(self.ohlcv.values['close'][idx])
                or self.ohlcv.values['open'][idx] == 0
                or self.ohlcv.values['high'][idx] == 0
                or self.ohlcv.values['low'][idx] == 0
                or self.ohlcv.values['close'][idx] == 0
        ):
            return False
        else:
            return True

    def _is_valid_vol(self, idx):
        if (
                self.ohlcv.values['volume'][idx] is None
                or numpy.isnan(self.ohlcv.values['volume'][idx])
                or self.ohlcv.values['volume'][idx] == 0
        ):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        raise NotImplementedError

    def check_entry_short(self, idx, last_exit_idx):
        raise NotImplementedError

    def get_order_vol(self, cash, idx, price, last_exit_idx):
        unit = Unit.get_unit(self.symbol)
        order_vol_from_cash = math.floor(cash / price / unit) * unit
        # 現在のキャンドルの出来高
        current_vol = self.ohlcv.values['volume'][idx]
        if ("N225minif" in self.symbol
                or "N225f" in self.symbol):
            current_vol = current_vol * unit
        if not self._is_valid_vol(idx):
            current_vol = -1
        # 出来高から発注数量を取得
        temp_vol = current_vol * self.order_vol_ratio
        order_vol_from_now = math.floor(temp_vol / unit) * unit
        if Unit.is_order_vol_infinity(self.symbol):
            if order_vol_from_cash > 1000000000000:
                vol = 1000000000000  # saidai 1tyou de iiyone.
            else:
                vol = order_vol_from_cash
        elif order_vol_from_cash < order_vol_from_now:
            vol = order_vol_from_cash
        else:
            vol = order_vol_from_now
        if vol < 0:
            vol = 0
        return vol

    def get_order_vol_from_ema(self, cash, idx, price, last_exit_idx):
        unit = Unit.get_unit(self.symbol)
        order_vol_from_cash = math.floor(cash / price / unit) * unit
        # 出来高の指数移動平均
        current_vol = self.ema.vol_ema[idx]
        if ("N225mini" in self.symbol
                or "N225f" in self.symbol):
            current_vol = current_vol * unit
        if not self._is_valid_vol(idx):
            current_vol = -1
        # 出来高から発注数量を取得
        temp_vol = current_vol * self.order_vol_ratio
        order_vol_from_ema = math.floor(temp_vol / unit) * unit
        if Unit.is_order_vol_infinity(self.symbol):
            vol = order_vol_from_cash
        elif current_vol == -1:
            vol = 0
        elif order_vol_from_cash < order_vol_from_ema:
            vol = order_vol_from_cash
        else:
            vol = order_vol_from_ema
        return vol

    def create_order_entry_long_stop_market_for_all_cash(self, cash, idx, last_exit_idx):
        raise NotImplementedError

    def create_order_entry_short_stop_market_for_all_cash(self, cash, idx, last_exit_idx):
        raise NotImplementedError

    def create_order_entry_long_stop_market(self, idx, last_exit_idx):
        raise NotImplementedError

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        raise NotImplementedError

    def create_order_entry_long_market_for_all_cash(self, cash, idx, last_exit_idx):
        raise NotImplementedError

    def create_order_entry_short_market_for_all_cash(self, cash, idx, last_exit_idx):
        raise NotImplementedError

    def get_indicators(self, idx, last_exit_idx):
        ind1 = None
        ind2 = None
        ind3 = None
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

    def get_vol_indicators(self, idx, last_exit_idx):
        ind1 = None
        ind2 = None
        ind3 = None
        ind4 = None
        ind5 = None
        return ind1, ind2, ind3, ind4, ind5

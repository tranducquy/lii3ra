import numpy


class ExitStrategyFactory:

    def create_strategy(self, ohlcv):
        raise NotImplementedError

    def optimization(self, ohlcv, rough=True):
        raise NotImplementedError


class ExitStrategy:
    """ポジションEXIT用のストラテジー"""
    def __init__(self, title, ohlcv):
        self.title = title
        self.ohlcv = ohlcv
        self.title = "ExitStrategy"

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

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

    def check_exit_long(self, pos_price, idx, entry_idx):
        raise NotImplementedError

    def check_exit_short(self, pos_price, idx, entry_idx):
        raise NotImplementedError

    def create_order_exit_long_stop_market(self, idx, entry_idx):
        raise NotImplementedError

    def create_order_exit_short_stop_market(self, idx, entry_idx):
        raise NotImplementedError

    def create_order_exit_long_market(self, idx, entry_idx):
        raise NotImplementedError

    def create_order_exit_short_market(self, idx, entry_idx):
        raise NotImplementedError

    def get_indicators(self, idx, entry_idx):
        ind1 = None
        ind2 = None
        ind3 = None
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

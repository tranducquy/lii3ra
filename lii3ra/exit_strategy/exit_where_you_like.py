from lii3ra.ordertype import OrderType
from lii3ra.exit_strategy.exit_strategy import ExitStrategyFactory
from lii3ra.exit_strategy.exit_strategy import ExitStrategy


class ExitWhereYouLikeFactory(ExitStrategyFactory):
    params = {
        # long_prof_exit, long_loss_exit, short_prof_exit, short_loss_exit
        "default": [10, 7, 10, 7]
    }

    rough_params = [
        [10, 7, 10, 7]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            long_prof_exit = self.params[s][0]
            long_loss_exit = self.params[s][1]
            short_prof_exit = self.params[s][2]
            short_loss_exit = self.params[s][3]
        else:
            long_prof_exit = self.params["default"][0]
            long_loss_exit = self.params["default"][1]
            short_prof_exit = self.params["default"][2]
            short_loss_exit = self.params["default"][3]
        return ExitWhereYouLike(ohlcv
                                , long_prof_exit
                                , long_loss_exit
                                , short_prof_exit
                                , short_loss_exit)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            #
            for p in self.rough_params:
                strategies.append(ExitWhereYouLike(ohlcv, p[0], p[1], p[2], p[3]))
        else:
            long_prof_exit_list = [i for i in range(3, 16, 3)]
            long_loss_exit_list = [i for i in range(3, 16, 3)]
            short_prof_exit_list = [i for i in range(3, 16, 3)]
            short_loss_exit_list = [i for i in range(3, 16, 3)]
            for long_prof_exit in long_prof_exit_list:
                for long_loss_exit in long_loss_exit_list:
                    strategies.append(ExitWhereYouLike(ohlcv
                                                       , long_prof_exit
                                                       , long_loss_exit
                                                       , self.params["default"][2]
                                                       , self.params["default"][3]))
            for short_prof_exit in short_prof_exit_list:
                for short_loss_exit in short_loss_exit_list:
                    strategies.append(ExitWhereYouLike(ohlcv
                                                       , self.params["default"][0]
                                                       , self.params["default"][1]
                                                       , short_prof_exit
                                                       , short_loss_exit))
        return strategies


class ExitWhereYouLike(ExitStrategy):
    """
    ロングの利益確定に指定した直近のバーの最高値、損切りでは直近のバーの最安値を使用する。
    ショートはその逆。
    指値注文で利確をして、逆指値注文で損切りする。
    """

    def __init__(self
                 , ohlcv
                 , long_prof_exit
                 , long_loss_exit
                 , short_prof_exit
                 , short_loss_exit):
        self.title = f"ExitWhereYouLike[{long_prof_exit:.0f},{long_loss_exit:.0f}][{short_prof_exit:.0f},{short_loss_exit:.0f}]"
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol
        self.long_prof_exit = long_prof_exit
        self.long_loss_exit = long_loss_exit
        self.short_prof_exit = short_prof_exit
        self.short_loss_exit = short_loss_exit
        self.long_prof_price = None
        self.long_loss_price = None

    def check_exit_long(self, pos_price, pos_vol, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        return OrderType.CLOSE_LONG_OCO

    def check_exit_short(self, pos_price, pos_vol, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        return OrderType.CLOSE_SHORT_OCO

    def create_order_exit_long_limit(self, idx, entry_idx):
        slice_idx = entry_idx - self.long_prof_exit
        if slice_idx < 0:
            slice_idx = 0
        high_bars = self.ohlcv.values['high'][slice_idx:entry_idx]
        max_high = high_bars.max()
        self.long_prof_price = max_high
        return max_high

    def create_order_exit_long_stop_market(self, idx, entry_idx):
        if not self._is_valid(idx):
            return 0.00
        slice_idx = entry_idx - self.long_loss_exit
        if slice_idx < 0:
            slice_idx = 0
        low_bars = self.ohlcv.values['low'][slice_idx:entry_idx]
        min_low = low_bars.min()
        self.long_loss_price = min_low
        return min_low

    def create_order_exit_short_limit(self, idx, entry_idx):
        slice_idx = entry_idx - self.short_prof_exit
        if slice_idx < 0:
            slice_idx = 0
        low_bars = self.ohlcv.values['low'][slice_idx:entry_idx]
        min_low = low_bars.min()
        self.short_prof_price = min_low
        return min_low

    def create_order_exit_short_stop_market(self, idx, entry_idx):
        if not self._is_valid(idx):
            return 0.00
        slice_idx = entry_idx - self.short_loss_exit
        if slice_idx < 0:
            slice_idx = 0
        high_bars = self.ohlcv.values['high'][slice_idx:entry_idx]
        max_high = high_bars.max()
        self.short_loss_price = max_high
        return max_high

    def create_order_exit_long_market(self, idx, entry_idx):
        return 0.00

    def create_order_exit_short_market(self, idx, entry_idx):
        return 0.00

    def get_indicators(self, idx, entry_idx):
        ind1 = self.long_prof_price if hasattr(self, "long_prof_price") else None
        ind2 = self.long_loss_price if hasattr(self, "long_loss_price") else None
        ind3 = self.short_prof_price if hasattr(self, "short_prof_price") else None
        ind4 = self.short_loss_price if hasattr(self, "short_loss_price") else None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

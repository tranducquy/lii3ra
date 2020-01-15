from lii3ra.ordertype import OrderType
from lii3ra.exit_strategy.exit_strategy import ExitStrategyFactory
from lii3ra.exit_strategy.exit_strategy import ExitStrategy


class GettingIsGoodFactory(ExitStrategyFactory):
    params = {
        # num_of_bars_long, num_of_bars_short, losscut_ratio
        "default": [3, 3, 0.05]
        , "^N225": [2, 1, 0.05]
        , "1570.T": [3, 3, 0.05]
        , "4523.T": [1, 1, 0.03]
        , "8876.T": [2, 4, 0.05]
        , "1568.T": [3, 1, 0.05]
        , "3038.T": [3, 1, 0.05]
        , "3088.T": [3, 3, 0.05]
    }

    rough_params = [
        [1, 1, 0.05]
        , [2, 2, 0.05]
        , [3, 3, 0.05]
        , [4, 4, 0.05]
        , [5, 5, 0.05]
        , [1, 1, 0.03]
        , [2, 2, 0.03]
        , [3, 3, 0.03]
        , [4, 4, 0.03]
        , [5, 5, 0.03]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            num_of_bars_long = self.params[s][0]
            num_of_bars_short = self.params[s][1]
            losscut_ratio = self.params[s][2]
        else:
            num_of_bars_long = self.params["default"][0]
            num_of_bars_short = self.params["default"][1]
            losscut_ratio = self.params["default"][2]
        return GettingIsGood(ohlcv
                             , num_of_bars_long
                             , num_of_bars_short
                             , losscut_ratio)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            #
            for p in self.rough_params:
                strategies.append(GettingIsGood(ohlcv, p[0], p[1], p[2]))
        else:
            num_of_bars_list = [i for i in range(1, 5)]
            losscut_ratio_list = [0.03, 0.05]
            for long_bars in num_of_bars_list:
                for short_bars in num_of_bars_list:
                    for losscut_ratio in losscut_ratio_list:
                        strategies.append(GettingIsGood(ohlcv
                                                        , long_bars
                                                        , short_bars
                                                        , losscut_ratio))
        return strategies


class GettingIsGood(ExitStrategy):
    """
    ポジションオープンから指定の回数連続して高値または安値を更新した場合、次のバーでExitする。
     - 注文方法:寄成
    """

    def __init__(self
                 , ohlcv
                 , num_of_bars_long=2
                 , num_of_bars_short=2
                 , losscut_ratio=0.03):
        self.title = f"GettingIsGood[{num_of_bars_long:.0f}][{num_of_bars_short:.0f}][{losscut_ratio:.2f}]"
        self.ohlcv = ohlcv
        self.symbol = ohlcv.symbol
        self.num_of_bars_long = num_of_bars_long
        self.num_of_bars_short = num_of_bars_short
        self.losscut_ratio = losscut_ratio
        self.up_count = 0
        self.down_count = 0

    def check_exit_long(self, pos_price, pos_vol, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        exit_long = True
        # 連騰チェック
        self.up_count = 0
        for i in range(self.num_of_bars_long):
            if entry_idx + self.num_of_bars_long <= idx:
                current_price = self.ohlcv.values['close'][idx - i]
                last_price = self.ohlcv.values['close'][idx - i - 1]
                if current_price < last_price:
                    exit_long = False
                    break
                self.up_count += 1
            else:
                exit_long = False
                break
        if exit_long:
            return OrderType.CLOSE_LONG_MARKET
        else:
            close = self.ohlcv.values['close'][idx]
            losscut_price = pos_price - (pos_price * self.losscut_ratio)
            # ロスカット
            if close < losscut_price:
                return OrderType.CLOSE_LONG_MARKET
            else:
                return OrderType.NONE_ORDER

    def check_exit_short(self, pos_price, pos_vol, idx, entry_idx):
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        exit_short = True
        # 続落チェック
        self.down_count = 0
        for i in range(self.num_of_bars_short):
            if entry_idx + self.num_of_bars_short <= idx:
                current_price = self.ohlcv.values['close'][idx - i]
                last_price = self.ohlcv.values['close'][idx - i - 1]
                if current_price > last_price:
                    exit_short = False
                    break
                self.down_count += 1
            else:
                exit_short = False
                break
        if exit_short:
            return OrderType.CLOSE_SHORT_MARKET
        else:
            close = self.ohlcv.values['close'][idx]
            losscut_price = pos_price + (pos_price * self.losscut_ratio)
            # ロスカット
            if close > losscut_price:
                return OrderType.CLOSE_SHORT_MARKET
            else:
                return OrderType.NONE_ORDER

    def create_order_exit_long_stop_market(self, idx, entry_idx):
        if not self._is_valid(idx):
            return 0.00
        # dummy
        return 0.00

    def create_order_exit_short_stop_market(self, idx, entry_idx):
        if not self._is_valid(idx):
            return 0.00
        # dummy
        return 0.00

    def create_order_exit_long_market(self, idx, entry_idx):
        return 0.00

    def create_order_exit_short_market(self, idx, entry_idx):
        return 0.00

    def get_indicators(self, idx, entry_idx):
        ind1 = self.num_of_bars_long
        ind2 = self.up_count
        ind3 = self.num_of_bars_short
        ind4 = self.down_count
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

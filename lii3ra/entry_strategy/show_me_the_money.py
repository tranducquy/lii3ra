from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.money_flow_indicator import MoneyFlowIndicator
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class ShowMeTheMoneyFactory(EntryStrategyFactory):
    params = {
        # mfi_length, oversold, overbought
        "default": [15, 20, 80]
    }

    rough_params = [
        [15, 20, 80]
    ]

    def create(self, ohlcv, optimization=False):
        strategies = []
        if not optimization:
            #
            s = ohlcv.symbol
            if s in self.params:
                mfi_length = self.params[s][0]
                oversold = self.params[s][1]
                overbought = self.params[s][2]
            else:
                mfi_length = self.params["default"][0]
                oversold = self.params["default"][1]
                overbought = self.params["default"][2]
            strategies.append(ShowMeTheMoney(ohlcv, mfi_length, oversold, overbought))
        else:
            mfi_list = [i for i in range(5, 25, 5)]
            oversold_list = [i for i in range(10, 100, 10)]
            overbought_list = [i for i in range(10, 100, 10)]
            for mfi in mfi_list:
                for oversold in oversold_list:
                    for overbought in overbought_list:
                        strategies.append(ShowMeTheMoney(ohlcv, mfi, oversold, overbought))
        return strategies


class ShowMeTheMoney(EntryStrategy):
    """
    MFIがしきい値をクロスした場合、エントリー
    """
    def __init__(self
                 , ohlcv
                 , mfi_length
                 , oversold
                 , overbought
                 , order_vol_ratio=0.01):
        self.title = f"ShowMeTheMoney[{mfi_length:.0f},{oversold:.0f},{overbought:.0f}]"
        self.ohlcv = ohlcv
        self.symbol = self.ohlcv.symbol
        self.mfi = MoneyFlowIndicator(ohlcv, mfi_length)
        self.oversold = oversold
        self.overbought = overbought
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.mfi.mfi[idx] == 0
        ):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        """
        MFIがしきい値を上にクロスした場合、次で成行きロング
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.mfi.period:
            return OrderType.NONE_ORDER
        before_mfi = self.mfi.mfi[idx-1]
        current_mfi = self.mfi.mfi[idx]
        before_condition = before_mfi < self.oversold
        current_condition = current_mfi > self.oversold
        if before_condition and current_condition:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        MFIがしきい値を下にクロスした場合、次で成行きショート
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.mfi.period:
            return OrderType.NONE_ORDER
        before_mfi = self.mfi.mfi[idx-1]
        current_mfi = self.mfi.mfi[idx]
        before_condition = before_mfi > self.overbought
        current_condition = current_mfi < self.overbought
        if before_condition and current_condition:
            return OrderType.MARKET_SHORT
        else:
            return OrderType.NONE_ORDER

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
        return 0.00

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        return 0.00

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
        ind1 = self.mfi.mfi[idx]
        ind2 = self.oversold
        ind3 = self.overbought
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

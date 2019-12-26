from lii3ra.ordertype import OrderType
from lii3ra.technical_indicator.relative_strength_index import RelativeStrengthIndex
from lii3ra.technical_indicator.average_directional_index import AverageDirectionalIndex
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class ThreeAmigosFactory(EntryStrategyFactory):
    params = {
        # adx_span, adx_threshold, rsi_span, rsi_threshold, lookback1, lookback2
        "default": [14, 0.25, 14, 50, 20, 10]
    }

    rough_params = [
        [14, 0.25, 14, 50, 20, 10]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            adx_span = self.params[s][0]
            adx_threshold = self.params[s][1]
            rsi_span = self.params[s][2]
            rsi_threshold = self.params[s][3]
            lookback1 = self.params[s][4]
            lookback2 = self.params[s][5]
        else:
            adx_span = self.params["default"][0]
            adx_threshold = self.params["default"][1]
            rsi_span = self.params["default"][2]
            rsi_threshold = self.params["default"][3]
            lookback1 = self.params["default"][4]
            lookback2 = self.params["default"][5]
        return ThreeAmigos(ohlcv, adx_span, adx_threshold, rsi_span, rsi_threshold, lookback1, lookback2)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            for p in self.rough_params:
                strategies.append(ThreeAmigos(ohlcv
                                              , p[0]
                                              , p[1]
                                              , p[2]
                                              , p[3]
                                              , p[4]
                                              , p[5]))
        else:
            adx_span_ary = [i for i in range(5, 25, 5)]
            adx_threshold_ary = [i for i in np.arange(0.10, 0.9, 0.1)]
            rsi_span_ary = [i for i in range(5, 25, 5)]
            rsi_threshold_ary = [i for i in range(20, 90, 10)]
            lookback1_ary = [i for i in range(5, 25, 5)]
            lookback2_ary = [i for i in range(5, 25, 5)]
            for adx_span in adx_span_ary:
                for adx_threshold in adx_threshold_ary:
                    strategies.append(ThreeAmigos(ohlcv
                                                  , adx_span, adx_threshold
                                                  , self.params["default"][2], self.params["default"][3]
                                                  , self.params["default"][4], self.params["default"][5]))
            for rsi_span in rsi_span_ary:
                for rsi_threshold in rsi_threshold_ary:
                    strategies.append(ThreeAmigos(ohlcv
                                                  , self.params["default"][0], self.params["default"][1]
                                                  , rsi_span, rsi_threshold
                                                  , self.params["default"][4], self.params["default"][5]))
            for lookback1 in lookback1_ary:
                for lookback2 in lookback2_ary:
                    strategies.append(ThreeAmigos(ohlcv
                                                  , self.params["default"][0], self.params["default"][1]
                                                  , self.params["default"][2], self.params["default"][3]
                                                  , lookback1, lookback2))
        return strategies


class ThreeAmigos(EntryStrategy):
    """
    RSI、ADX、短期および長期のモメンタムを使用してエントリーする。
    最適化しすぎないほうが良いらしい。
    """

    def __init__(self
                 , ohlcv
                 , adx_span
                 , adx_threshold
                 , rsi_span
                 , rsi_threshold
                 , lookback1
                 , lookback2
                 , order_vol_ratio=0.01):
        self.title = f"ThreeAmigos[{adx_span:.0f},{adx_threshold:.0f}][{rsi_span:.0f},{rsi_threshold:.0f}][{lookback1:.0f},{lookback2:.0f}]"
        self.ohlcv = ohlcv
        self.symbol = self.ohlcv.symbol
        self.adx = AverageDirectionalIndex(ohlcv, adx_span)
        self.adx_threshold = adx_threshold
        self.rsi = RelativeStrengthIndex(ohlcv, rsi_span)
        self.rsi_threshold = rsi_threshold
        self.lookback1 = lookback1
        self.lookback2 = lookback2
        self.order_vol_ratio = order_vol_ratio

    def _is_indicator_valid(self, idx):
        if (
                self.adx.adx[idx] == 0
                or self.rsi.rsi[idx] == 0
        ):
            return False
        else:
            return True

    def check_entry_long(self, idx, last_exit_idx):
        """
        ADXが閾値を上回っており、RSIが閾値を下回っており、モメンタムが上昇トレンドであれば次で成行ロング
vars: ADXLength(14), RSILength(14), lookbackBig(20), lookbackshort(10);
If ADX(ADXLength)>25 then begin
     If RSI(close,RSILength)<50 and close<close[lookbackBig] and close>close[lookbackshort] then buy next bar at market;
     If RSI(close,RSILength)>50 and close>close[lookbackBig] and close<close[lookbackshort] then sellshort next bar at market;
end;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.adx.adx_span \
                or idx <= self.rsi.span \
                or idx <= self.lookback1 \
                or idx <= self.lookback2:
            return OrderType.NONE_ORDER
        if self.adx.adx[idx] > self.adx_threshold:
            rsi_value = self.rsi.rsi[idx]
            close = self.ohlcv.values['close'][idx]
            close_lookback1 = self.ohlcv.values['close'][idx-self.lookback1]
            close_lookback2 = self.ohlcv.values['close'][idx-self.lookback2]
            rsi_condition = rsi_value < self.rsi_threshold
            lookback1_condition = close < close_lookback1
            lookback2_condition = close > close_lookback2
            if rsi_condition and lookback1_condition and lookback2_condition:
                return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        ADXが閾値を上回っており、RSIが閾値を上回っており、モメンタムが下降トレンドであれば次で成行ショート
     If RSI(close,RSILength)>50 and close>close[lookbackBig] and close<close[lookbackshort] then sellshort next bar at market;
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if not self._is_indicator_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.adx.adx_span \
                or idx <= self.rsi.span \
                or idx <= self.lookback1 \
                or idx <= self.lookback2:
            return OrderType.NONE_ORDER
        if self.adx.adx[idx] > self.adx_threshold:
            rsi_value = self.rsi.rsi[idx]
            close = self.ohlcv.values['close'][idx]
            close_lookback1 = self.ohlcv.values['close'][idx-self.lookback1]
            close_lookback2 = self.ohlcv.values['close'][idx-self.lookback2]
            rsi_condition = rsi_value > self.rsi_threshold
            lookback1_condition = close > close_lookback1
            lookback2_condition = close < close_lookback2
            if rsi_condition and lookback1_condition and lookback2_condition:
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
        ind1 = self.adx.adx[idx]
        ind2 = self.adx_threshold
        ind3 = self.rsi.rsi[idx]
        ind4 = self.rsi_threshold
        ind5 = self.ohlcv.values['close'][idx-self.lookback1] if idx > self.lookback1 else None
        ind6 = self.ohlcv.values['close'][idx-self.lookback2] if idx > self.lookback2 else None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

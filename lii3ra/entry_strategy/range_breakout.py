import numpy as np
from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy
from lii3ra.ohlcv import Ohlcv
from lii3ra.technical_indicator.average_true_range import AverageTrueRange


class RangeBreakoutFactory(EntryStrategyFactory):
    params = {
        # begin_time, end_time, atr_span_1d, xfl, xfs
        "default": ["084500", "100000", 10, 1.0, 1.0]
    }

    rough_params = [
        ["084500", "100000", 10, 1.0, 1.0]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            begin_time = self.params[s][0]
            end_time = self.params[s][1]
            atr_span_1d = self.params[s][2]
            xfl = self.params[s][3]
            xfs = self.params[s][4]
        else:
            begin_time = self.params["default"][0]
            end_time = self.params["default"][1]
            atr_span_1d = self.params["default"][2]
            xfl = self.params["default"][3]
            xfs = self.params["default"][4]
        return RangeBreakout(ohlcv, begin_time, end_time, atr_span_1d, xfl, xfs)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            #
            for p in self.rough_params:
                strategies.append(RangeBreakout(ohlcv
                                                , p[0]
                                                , p[1]
                                                , p[2]
                                                , p[3]
                                                , p[4]))
        else:
            time_list = [
                ["080000", "090000"]
                , ["090000", "100000"]
                , ["100000", "110000"]
                , ["110000", "120000"]
                , ["110000", "120000"]
                , ["120000", "130000"]
                , ["130000", "140000"]
                , ["140000", "150000"]
                , ["150000", "160000"]
                , ["160000", "170000"]
                , ["170000", "180000"]
                , ["180000", "190000"]
                , ["190000", "200000"]
                , ["200000", "210000"]
                , ["210000", "220000"]
                , ["220000", "230000"]
                , ["230000", "000000"]
                , ["000000", "010000"]
                , ["010000", "020000"]
                , ["020000", "030000"]
                , ["030000", "040000"]
                , ["040000", "050000"]
                , ["050000", "060000"]
                , ["060000", "070000"]
                , ["070000", "080000"]
            ]
            atr_span_1d_list = [i for i in range(3, 16, 3)]
            xfl_list = [i for i in np.arange()]
            # xfs_list = [i for i in np.arange()]
            for times in time_list:
                for atr_span in atr_span_1d_list:
                    for xfl in xfl_list:
                        strategies.append(RangeBreakout(ohlcv
                                                        , times[0]
                                                        , times[1]
                                                        , atr_span
                                                        , xfl
                                                        , xfl))
        return strategies


class RangeBreakout(EntryStrategy):
    """
    当日始値から日足でレンジを判定し、指定時間内に限り分足で逆指値注文する
     * 日中のみ有効なエントリー
     * 分足が必要
    """

    def __init__(self
                 , ohlcv
                 , begin_time
                 , end_time
                 , atr_span_1d
                 , xfl
                 , xfs
                 , order_vol_ratio=0.01):
        self.title = f"RangeBreakout[{begin_time},{end_time}][{atr_span_1d:.0f},{xfl:.2f},{xfs:.2f}]"
        self.ohlcv = ohlcv
        self.begin_time = begin_time
        self.end_time = end_time
        self.xfl = xfl
        self.xfs = xfs
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio
        self.firstday = None
        self.trade_days = None
        self.today_open = None
        self.atr_value = None
        self.ohlcv_1d = Ohlcv(self.symbol, "1d", self.ohlcv.start_date, self.ohlcv.end_date)
        self.atr_1d = AverageTrueRange(self.ohlcv_1d, atr_span_1d)

    def is_firstday(self, idx):
        current_day = self.ohlcv.values['time'][idx].strftime("%Y%m%d")
        if self.firstday is None:
            self.firstday = current_day
            return True
        if self.firstday == current_day:
            return True
        else:
            return False

    def is_entrytime(self, idx):
        current_time = self.ohlcv.values['time'][idx].strftime("%H%M%S")
        if self.begin_time <= current_time <= self.end_time:
            return True
        else:
            return False

    def check_entry_long(self, idx, last_exit_idx):
        """
        時間内ならOCOにより逆指値
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if self.is_firstday(idx):
            return OrderType.NONE_ORDER
        if not self.is_entrytime(idx):
            return OrderType.NONE_ORDER
        # 日足始値取得
        self.today_open = self._get_today_open(idx)
        # 日足ATR取得
        self.atr_value = self._get_atr_1d(idx)
        if self.today_open is None or self.atr_value is None:
            return OrderType.NONE_ORDER
        else:
            return OrderType.OCO

    def check_entry_short(self, idx, last_exit_idx):
        """
        時間内ならOCOにより逆指値
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if self.is_firstday(idx):
            return OrderType.NONE_ORDER
        if not self.is_entrytime(idx):
            return OrderType.NONE_ORDER
        # 日足始値取得
        self.today_open = self._get_today_open(idx)
        # 日足ATR取得
        self.atr_value = self._get_atr_1d(idx)
        if self.today_open is None or self.atr_value is None:
            return OrderType.NONE_ORDER
        else:
            return OrderType.OCO

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
        return self.today_open + self.atr_value * self.xfl

    def create_order_entry_short_stop_market(self, idx, last_exit_idx):
        if not self._is_valid(idx):
            return -1
        return self.today_open - self.atr_value * self.xfl

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
        ind1 = None
        ind2 = None
        ind3 = None
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

    def _get_today_open(self, idx):
        # TODO:営業日
        current_day = self.ohlcv.values['time'][idx].date()
        opens = self.ohlcv_1d.values['open'][self.ohlcv_1d.values['time'].dt.date == current_day]
        today_open = 0
        if opens.size == 1:
            for o in opens:
                today_open = o
        else:
            today_open = 0
        return today_open

    def _get_before_day_1d(self, idx):
        if self.trade_days is None:
            self.trade_days = self.ohlcv_1d.values['time'].dt.date
        current_day = self.ohlcv.values['time'][idx].date()
        past_trade_days = self.trade_days[self.trade_days < current_day]
        before_day = past_trade_days.max()
        return before_day

    def _get_atr_1d(self, idx):
        before_day = self._get_before_day_1d(idx)
        dt = self.ohlcv_1d.values.index[self.ohlcv_1d.values['time'].dt.date == before_day]
        if dt is None or dt.size == 0:
            return None
        index = 0
        for i in dt:
            index = i
        atr_value = self.atr_1d.atr[index]
        return atr_value

from lii3ra.ordertype import OrderType
from lii3ra.entry_strategy.entry_strategy import EntryStrategyFactory
from lii3ra.entry_strategy.entry_strategy import EntryStrategy


class IntroducingSerialCorrelationFactory(EntryStrategyFactory):
    params = {
        # lookback, winner_waiting_period, loser_waiting_period
        "default": [15, 5, 20]
    }

    rough_params = [
        [15, 5, 20]
    ]

    def create_strategy(self, ohlcv):
        s = ohlcv.symbol
        if s in self.params:
            lookback = self.params[s][0]
            winner_waiting_period = self.params[s][1]
            loser_waiting_period = self.params[s][2]
        else:
            lookback = self.params["default"][0]
            winner_waiting_period = self.params["default"][1]
            loser_waiting_period = self.params["default"][2]
        return IntroducingSerialCorrelation(ohlcv, lookback, winner_waiting_period, loser_waiting_period)

    def optimization(self, ohlcv, rough=True):
        strategies = []
        if rough:
            for p in self.rough_params:
                strategies.append(IntroducingSerialCorrelation(ohlcv
                                                 , p[0]
                                                 , p[1]
                                                 , p[2]))
        else:
            lookback_list = [i for i in range(3, 25, 2)]
            winner_wait = [i for i in range(2, 20, 2)]
            loser_wait = [i for i in range(5, 30, 3)]
            for lookback in lookback_list:
                for winner in winner_wait:
                    for loser in loser_wait:
                        strategies.append(IntroducingSerialCorrelation(ohlcv, lookback, winner, loser))
        return strategies


class IntroducingSerialCorrelation(EntryStrategy):
    """
    INTRODUCING SERIAL CORRELATION
Var: xbars(15); // lookback period
//if last position was profitable, wait 5 bars before taking a new trade
// if last trade was a loser, wait 20 bars before taking the next signal
//allows the first trade in the backtest to occur
If (
(PositionProfit(1)>0 and BarsSinceExit(1)>=5)
or (PositionProfit(1)<=0 and BarsSinceExit(1)>=20)
or TotalTrades=0
) then begin
    if Close = Lowest( Close, xbars ) then buy next bar at market;
    if Close = Highest( Close, xbars ) then SellShort next bar at market;
end;
    """

    def __init__(self
                 , ohlcv
                 , lookback
                 , winner_waiting_period=5
                 , loser_waiting_period=20
                 , order_vol_ratio=0.01):
        self.title = f"IntroSerial[{lookback:.0f},{winner_waiting_period:.0f},{loser_waiting_period:.0f}]"
        self.ohlcv = ohlcv
        self.lookback = lookback
        self.winner_waiting_period = winner_waiting_period
        self.loser_waiting_period = loser_waiting_period
        self.symbol = self.ohlcv.symbol
        self.order_vol_ratio = order_vol_ratio

    def check_entry_long(self, idx, last_exit_idx):
        """
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.lookback:
            return OrderType.NONE_ORDER
        if len(self.position.exit_positions_profit) == 0:
            initial_trade = True
            last_exit_profit = 0
        else:
            initial_trade = False
            last_exit_profit = self.position.exit_positions_profit[-1]
        close = self.ohlcv.values['close'][idx]
        lowest_close = self.ohlcv.values['close'][idx - self.lookback:idx + 1].min()
        # highest_close = self.ohlcv.values['close'][idx - self.lookback:idx + 1].max()
        long_flg1 = initial_trade \
                    or (last_exit_profit > 0 and idx - last_exit_idx >= self.winner_waiting_period) \
                    or (last_exit_profit <= 0 and idx - last_exit_idx >= self.loser_waiting_period)
        long_flg2 = close == lowest_close
        # long_flg2 = close == highest_close
        if long_flg1 and long_flg2:
            return OrderType.MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_entry_short(self, idx, last_exit_idx):
        """
        """
        if not self._is_valid(idx):
            return OrderType.NONE_ORDER
        if idx <= self.lookback:
            return OrderType.NONE_ORDER
        if len(self.position.exit_positions_profit) == 0:
            initial_trade = True
            last_exit_profit = 0
        else:
            initial_trade = False
            last_exit_profit = self.position.exit_positions_profit[-1]
        close = self.ohlcv.values['close'][idx]
        highest_close = self.ohlcv.values['close'][idx - self.lookback:idx + 1].max()
        # lowest_close = self.ohlcv.values['close'][idx - self.lookback:idx + 1].min()
        short_flg1 = initial_trade \
                     or (last_exit_profit > 0 and idx - last_exit_idx >= self.winner_waiting_period) \
                     or (last_exit_profit <= 0 and idx - last_exit_idx >= self.loser_waiting_period)
        short_flg2 = close == highest_close
        # short_flg2 = close == lowest_close
        if short_flg1 and short_flg2:
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
        ind1 = None
        ind2 = None
        ind3 = None
        ind4 = None
        ind5 = None
        ind6 = None
        ind7 = None
        return ind1, ind2, ind3, ind4, ind5, ind6, ind7

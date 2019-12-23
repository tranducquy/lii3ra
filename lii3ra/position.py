from lii3ra import order
from lii3ra.positiontype import PositionType
from lii3ra.ordertype import OrderType


class Position:
    def __init__(self, assets):
        self.assets = assets
        self.position = PositionType.NOTHING
        self.pos_price = 0
        self.pos_vol = 0
        self.exit_price = 0
        self.exit_vol = 0
        self.order = None
        self.win_count = 0
        self.lose_count = 0
        self.profit_value_sum = 0
        self.profit_rate_sum = 0
        self.summary = {
            'WinCount': 0
            , 'LoseCount': 0
            , 'WinValue': 0.00
            , 'LoseValue': 0.00
            , 'InitValue': self.assets.initial_cash
            , 'LastValue': self.assets.initial_cash
            , 'ProfitRateSummary': 0.00
            , 'PositionHavingSec': 0
            , 'LongWinCount': 0
            , 'LongLoseCount': 0
            , 'LongWinValue': 0.00
            , 'LongLoseValue': 0.00
            , 'LongProfitRateSummary': 0.00
            , 'LongPositionHavingSec': 0
            , 'ShortWinCount': 0
            , 'ShortLoseCount': 0
            , 'ShortWinValue': 0.00
            , 'ShortLoseValue': 0.00
            , 'ShortProfitRateSummary': 0.00
            , 'ShortPositionHavingSec': 0
            , 'Fee': 0.0
            , 'SpreadFee': 0.0
        }
        self.entry_idx = 0
        self.last_exit_idx = 0
        self.exit_positions_profit = []

    def get_position(self):
        return self.position

    def create_order_entry_long_limit(self, idx, create_time, price, vol):
        self.order = order.Order()
        self.order.set_order(create_time, OrderType.LIMIT_LONG, price, vol)

    def create_order_entry_short_limit(self, idx, create_time, price, vol):
        self.order = order.Order()
        self.order.set_order(create_time, OrderType.LIMIT_SHORT, price, vol)

    def create_order_entry_long_stop_market(self, idx, create_time, price, vol):
        self.order = order.Order()
        self.order.set_order(create_time, OrderType.STOP_MARKET_LONG, price, vol)

    def create_order_entry_short_stop_market(self, idx, create_time, price, vol):
        self.order = order.Order()
        self.order.set_order(create_time, OrderType.STOP_MARKET_SHORT, price, vol)

    def create_order_entry_long_market(self, idx, create_time, price, vol):
        self.order = order.Order()
        self.order.set_order(create_time, OrderType.MARKET_LONG, price, vol)

    def create_order_entry_short_market(self, idx, create_time, price, vol):
        self.order = order.Order()
        self.order.set_order(create_time, OrderType.MARKET_SHORT, price, vol)

    def create_order_exit_long_stop_market(self, idx, create_time, price, vol):
        self.order = order.Order()
        self.order.set_order(create_time, OrderType.CLOSE_LONG_STOP_MARKET, price, vol)

    def create_order_exit_short_stop_market(self, idx, create_time, price, vol):
        self.order = order.Order()
        self.order.set_order(create_time, OrderType.CLOSE_SHORT_STOP_MARKET, price, vol)

    def create_order_exit_long_market(self, idx, create_time, price, vol):
        self.order = order.Order()
        self.order.set_order(create_time, OrderType.CLOSE_LONG_MARKET, price, vol)

    def create_order_exit_short_market(self, idx, create_time, price, vol):
        self.order = order.Order()
        self.order.set_order(create_time, OrderType.CLOSE_SHORT_MARKET, price, vol)

    def create_order_oco(self, idx, create_time, stop_price_long, stop_price_short, vol):
        long_order = order.Order()
        long_order.set_order(create_time, OrderType.STOP_MARKET_LONG, stop_price_long, vol)
        short_order = order.Order()
        short_order.set_order(create_time, OrderType.STOP_MARKET_SHORT, stop_price_short, vol * -1)
        self.order = order.Order()
        self.order.set_oco_order(create_time, OrderType.OCO, long_order, short_order)

    def create_order_exit_long_oco(self, idx, create_time, limit_price, stop_market_price, vol):
        limit_order = order.Order()
        limit_order.set_order(create_time, OrderType.CLOSE_LONG_LIMIT, limit_price, vol)
        stop_market_order = order.Order()
        stop_market_order.set_order(create_time, OrderType.CLOSE_LONG_STOP_MARKET, stop_market_price, vol)
        self.order = order.Order()
        self.order.set_oco_order(create_time, OrderType.CLOSE_LONG_OCO, limit_order, stop_market_order)

    def create_order_exit_short_oco(self, idx, create_time, limit_price, stop_market_price, vol):
        limit_order = order.Order()
        limit_order.set_order(create_time, OrderType.CLOSE_SHORT_LIMIT, limit_price, vol)
        stop_market_order = order.Order()
        stop_market_order.set_order(create_time, OrderType.CLOSE_SHORT_STOP_MARKET, stop_market_price, vol)
        self.order = order.Order()
        self.order.set_oco_order(create_time, OrderType.CLOSE_SHORT_OCO, limit_order, stop_market_order)

    def call_order(self, idx, order_time):
        self.order.order(order_time)

    def clear_order(self, idx):
        self.order = None

    def entry_long(self, idx, candle_time, order_price, order_vol):
        self.position = PositionType.LONG
        self.order.price = order_price
        self.pos_price = self.order.price
        self.pos_vol = order_vol
        # self.pos_vol = math.floor(self.cash / order_price)
        # self.before_cash = self.cash
        # self.cash = round(self.cash - self.pos_vol * self.pos_price, 2)
        self.assets.entry_long(self.pos_price, self.pos_vol)
        self.order.execution_order(candle_time)
        self.order_time = self.order.order_time
        self.entry_idx = idx

    def entry_short(self, idx, candle_time, order_price, order_vol):
        self.position = PositionType.SHORT
        self.order.price = order_price
        self.pos_price = self.order.price
        self.pos_vol = order_vol
        # self.pos_vol = math.floor((self.cash / order_price) * -1)
        # self.before_cash = self.cash
        # self.cash = round(self.cash + (self.pos_vol*-1) * self.pos_price, 2)
        self.assets.entry_short(self.pos_price, self.pos_vol)
        self.order.execution_order(candle_time)
        self.order_time = self.order.order_time
        self.entry_idx = idx

    def exit_long(self, idx, candle_time, order_price):
        self.position = PositionType.NOTHING
        self.order.price = order_price
        self.exit_price = self.order.price
        self.exit_vol = self.pos_vol
        # self.cash = round(self.cash + (self.pos_vol * self.pos_price), 2)
        self.assets.exit_long(self.exit_price, self.exit_vol)
        self.pos_vol = 0
        self.order.execution_order(candle_time)
        self.exit_time = self.order.exit_order_time
        self.last_exit_idx = idx
        # TODO:candleの本数か、分か、秒か
        # entry_time = datetime.datetime.strptime(self.order_time, "%Y-%m-%d")
        # exit_time = datetime.datetime.strptime(self.exit_time, "%Y-%m-%d")
        entry_time = self.order_time
        exit_time = self.exit_time
        self.summary['PositionHavingSec'] += (exit_time - entry_time).seconds
        self.summary['LongPositionHavingSec'] += (exit_time - entry_time).seconds

    def exit_short(self, idx, candle_time, order_price):
        self.position = PositionType.NOTHING
        self.order.price = order_price
        self.exit_price = self.order.price
        self.exit_vol = self.pos_vol
        # self.cash = round(self.cash + (self.pos_vol * self.pos_price), 2)
        self.assets.exit_short(self.exit_price, self.exit_vol)
        self.pos_vol = 0
        self.order.execution_order(candle_time)
        self.exit_time = self.order.exit_order_time
        self.last_exit_idx = idx
        # TODO:candleの本数か、分か、秒か
        # entry_time = datetime.datetime.strptime(self.order_time, "%Y-%m-%d")
        # exit_time = datetime.datetime.strptime(self.exit_time, "%Y-%m-%d")
        entry_time = self.order_time
        exit_time = self.exit_time
        self.summary['PositionHavingSec'] += (exit_time - entry_time).seconds
        self.summary['ShortPositionHavingSec'] += (exit_time - entry_time).seconds

    def save_trade_performance(self, idx, position_type):
        win = 0
        lose = 0
        if self.assets.before_cash < self.assets.cash:
            win = 1
        else:
            lose = 1
        # profit_value = self.assets.cash - self.assets.before_cash
        # profit_rate = profit_value / self.assets.before_cash * 100
        profit_value = (self.exit_price * self.exit_vol) - (
                    self.pos_price * self.exit_vol) - self.assets.last_fee - self.assets.last_spread_fee
        self.exit_positions_profit.append(profit_value)
        if self.pos_price != 0 and self.exit_vol != 0 and profit_value != 0:
            profit_rate = profit_value / abs(self.pos_price * self.exit_vol)
        else:
            profit_rate = 0
        trade_performance = {
            'before_cash': self.assets.before_cash
            , 'cash': self.assets.cash
            , 'win': win
            , 'lose': lose
            , 'profit_value': profit_value
            , 'profit_rate': profit_rate
            , 'fee': self.assets.last_fee
            , 'spread_fee': self.assets.last_spread_fee
        }
        self.summary['WinCount'] += win
        self.summary['LoseCount'] += lose
        if position_type == PositionType.LONG:
            self.summary['LongWinCount'] += win
            self.summary['LongLoseCount'] += lose
        if position_type == PositionType.SHORT:
            self.summary['ShortWinCount'] += win
            self.summary['ShortLoseCount'] += lose

        if win == 1:
            self.summary['WinValue'] += profit_value
            if position_type == PositionType.LONG:
                self.summary['LongWinValue'] += profit_value
            if position_type == PositionType.SHORT:
                self.summary['ShortWinValue'] += profit_value
        else:
            self.summary['LoseValue'] += abs(profit_value)
            if position_type == PositionType.LONG:
                self.summary['LongLoseValue'] += abs(profit_value)
            if position_type == PositionType.SHORT:
                self.summary['ShortLoseValue'] += abs(profit_value)
        self.summary['LastValue'] = self.assets.cash + (self.pos_vol * self.pos_price)
        self.summary['ProfitRateSummary'] += profit_rate
        if position_type == PositionType.LONG:
            self.summary['LongProfitRateSummary'] += profit_rate
        if position_type == PositionType.SHORT:
            self.summary['ShortProfitRateSummary'] += profit_rate
        self.summary['Fee'] += self.assets.last_fee
        self.summary['SpreadFee'] += self.assets.last_spread_fee
        return trade_performance

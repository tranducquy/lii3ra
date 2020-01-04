# -*- coding: utf-8 -*-

import numpy
from lii3ra.mylogger import Logger
from lii3ra.position import Position
from lii3ra.positiontype import PositionType
from lii3ra.ordertype import OrderType
from lii3ra.orderstatus import OrderStatus
from lii3ra.backtest_dumper import BacktestDumper
from lii3ra.exit_strategy.end_of_bar import EndOfBar


class Market:
    def __init__(self, logger=None):
        if logger is None:
            self.logger = Logger().myLogger()
        else:
            self.logger = logger
        self.dumper = BacktestDumper()

    def simulator_run(self, ohlcv, entry_strategy, exit_strategy, asset):
        symbol = ohlcv.symbol
        p = Position(asset)
        entry_strategy.set_position(p)
        backtest_history = list()
        for idx, high in enumerate(ohlcv.values['high']):
            current_position = p.get_position()
            low = ohlcv.values['low'][idx]
            open_price = ohlcv.values['open'][idx]
            close_price = ohlcv.values['close'][idx]
            candle_time = ohlcv.values['time'][idx]
            order_info = {'create_time': None, 'order_time': None, 'order_type': 0, 'order_status': 0, 'vol': 0.00,
                          'price': 0.00}
            call_order_info = {'create_time': None, 'order_time': None, 'order_type': 0, 'order_status': 0, 'vol': 0.00,
                               'price': 0.00}
            execution_order_info = {'exit_order_time': None, 'order_type': 0, 'order_status': 0, 'vol': 0.00,
                                    'price': 0.00}
            execution_order_info2 = {'exit_order_time': None, 'order_type': 0, 'order_status': 0, 'vol': 0.00,
                                     'price': 0.00}
            trade_performance = {'profit_value': 0.00, 'profit_rate': 0.00, 'fee': 0.0, 'spread_fee': 0.0}
            try:
                if (open_price is None
                        or low is None
                        or high is None
                        or numpy.isnan(open_price)
                        or numpy.isnan(low)
                        or numpy.isnan(high)):
                    self.logger.warning('[%s][%d] ohlc is None or nan' % (symbol, idx))
                    continue
            except Exception as err:
                self.logger.error('[%s][%d] ohlc is exception value:[%s]' % (symbol, idx, err))
                continue

            # キャンドルひとつぶんの処理開始
            # 注文を呼び出す
            if p.order is not None:
                p.call_order(idx, candle_time)
                self.set_order_info(call_order_info, p.order)
            # 注文がある場合、約定判定
            if current_position == PositionType.NOTHING and p.order is not None:
                if p.order.order_type == OrderType.LIMIT_LONG:
                    # 約定判定
                    if p.order.price == -1:
                        self.logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                        p.order.fail_order()
                    elif p.order.vol == 0:
                        p.order.fail_order()
                    elif low <= p.order.price:
                        order_vol = p.order.vol
                        order_price = p.order.price
                        p.entry_long(idx, candle_time, order_price, order_vol)
                    else:
                        p.order.fail_order()
                    self.set_order_info(execution_order_info, p.order)
                if p.order.order_type == OrderType.LIMIT_SHORT:
                    # 約定判定
                    if p.order.price == -1:
                        self.logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                        p.order.fail_order()
                    elif p.order.vol == 0:
                        p.order.fail_order()
                    elif high >= p.order.price:
                        order_price = p.order.price
                        order_vol = p.order.vol
                        p.entry_short(idx, candle_time, p.order.price, order_vol)
                    else:
                        p.order.fail_order()
                    self.set_order_info(execution_order_info, p.order)
                if p.order.order_type == OrderType.STOP_MARKET_LONG:
                    # 約定判定
                    order_price = 0
                    if p.order.price == -1:
                        self.logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                        p.order.fail_order()
                    elif p.order.vol == 0:
                        p.order.fail_order()
                    elif high >= p.order.price and open_price >= p.order.price:  # 寄り付きが高値の場合
                        # 最大volまで購入
                        order_price = open_price
                        (margin_cash, _) = asset.get_margin_cash(symbol)
                        order_vol = entry_strategy.get_order_vol(margin_cash, idx, order_price, p.last_exit_idx)
                        p.entry_long(idx, candle_time, order_price, order_vol)
                    elif high >= p.order.price:
                        order_vol = p.order.vol
                        order_price = p.order.price
                        p.entry_long(idx, candle_time, order_price, order_vol)
                    else:
                        p.order.fail_order()
                    self.set_order_info(execution_order_info, p.order)
                    # Open約定期間中のロスカット
                    if p.order.order_status == OrderStatus.EXECUTION:
                        losscut_price = order_price - (order_price * asset.get_losscut_ratio(symbol))
                        if low <= losscut_price:
                            p.order.order_type = OrderType.CLOSE_LONG_STOP_MARKET
                            # call_order_info['order_type'] = OrderType.CLOSE_LONG_STOP_MARKET
                            p.exit_long(idx, candle_time, losscut_price)
                            trade_performance = p.save_trade_performance(idx, PositionType.LONG)
                            self.set_order_info(execution_order_info2, p.order)
                elif p.order.order_type == OrderType.STOP_MARKET_SHORT:
                    # 約定判定
                    if p.order.price == -1:
                        self.logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                        p.order.fail_order()
                    elif p.order.vol == 0:
                        p.order.fail_order()
                    elif low <= p.order.price and open_price <= p.order.price:  # 寄り付きが安値の場合
                        # 最大volまで売却
                        order_price = open_price
                        (margin_cash, _) = asset.get_margin_cash(symbol)
                        order_vol = entry_strategy.get_order_vol(margin_cash, idx, order_price, p.last_exit_idx)
                        order_vol = order_vol * -1
                        p.entry_short(idx, candle_time, order_price, order_vol)
                    elif low <= p.order.price:
                        order_price = p.order.price
                        order_vol = p.order.vol
                        p.entry_short(idx, candle_time, p.order.price, order_vol)
                    else:
                        p.order.fail_order()
                    self.set_order_info(execution_order_info, p.order)
                    # Open約定期間中のロスカット
                    if p.order.order_status == OrderStatus.EXECUTION:
                        losscut_price = order_price + (order_price * asset.get_losscut_ratio(symbol))
                        if high >= losscut_price:
                            p.order.order_type = OrderType.CLOSE_SHORT_STOP_MARKET
                            p.exit_short(idx, candle_time, losscut_price)
                            trade_performance = p.save_trade_performance(idx, PositionType.SHORT)
                            self.set_order_info(execution_order_info2, p.order)
                elif p.order.order_type == OrderType.MARKET_LONG:
                    # 約定判定
                    if p.order.price == -1:
                        self.logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                        p.order.fail_order()
                    else:
                        # 最大volまで購入
                        order_vol = asset.get_max_vol(open_price)
                        p.entry_long(idx, candle_time, open_price, order_vol)
                    self.set_order_info(execution_order_info, p.order)
                elif p.order.order_type == OrderType.MARKET_SHORT:
                    # 約定判定
                    if p.order.price == -1:
                        self.logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                        p.order.fail_order()
                    else:
                        # 最大volまで売却
                        order_vol = asset.get_max_vol(open_price) * -1
                        p.entry_short(idx, candle_time, open_price, order_vol)
                    self.set_order_info(execution_order_info, p.order)
                elif p.order.order_type == OrderType.OCO:
                    # TODO:OCO STOP_LIMIT
                    # OCO1
                    if p.order.oco_order1.order_type == OrderType.STOP_MARKET_LONG:
                        # TODO:リファクタリング
                        oco_order1 = p.order.oco_order1
                        # 約定判定
                        if oco_order1.price == -1:
                            self.logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, oco_order1.price))
                            p.order.fail_order()
                        elif p.order.vol == 0:
                            p.order.fail_order()
                        elif high >= oco_order1.price and open_price >= oco_order1.price:  # 寄り付きが高値の場合
                            # 最大volまで購入
                            order_price = open_price
                            (margin_cash, _) = asset.get_margin_cash(symbol)
                            order_vol = entry_strategy.get_order_vol(margin_cash, idx, order_price, p.last_exit_idx)
                            p.entry_long(idx, candle_time, order_price, order_vol)
                        elif high >= oco_order1.price:
                            order_vol = oco_order1.vol
                            order_price = oco_order1.price
                            p.entry_long(idx, candle_time, order_price, order_vol)
                        else:
                            p.order.fail_order()
                        self.set_order_info(execution_order_info, oco_order1)
                        # Open約定期間中のロスカット
                        if p.order.order_status == OrderStatus.EXECUTION:
                            losscut_price = order_price - (order_price * asset.get_losscut_ratio(symbol))
                            if low <= losscut_price:
                                oco_order1.order_type = OrderType.CLOSE_LONG_STOP_MARKET
                                # call_order_info['order_type'] = OrderType.CLOSE_LONG_STOP_MARKET
                                p.exit_long(idx, candle_time, losscut_price)
                                trade_performance = p.save_trade_performance(idx, PositionType.LONG)
                                self.set_order_info(execution_order_info2, oco_order1)
                    # OCO2
                    if not p.order.oco_order1.order_status == OrderStatus.EXECUTION and p.order.oco_order2.order_type == OrderType.STOP_MARKET_SHORT:
                        # TODO:リファクタリング
                        oco_order2 = p.order.oco_order2
                        # 約定判定
                        if oco_order2.price == -1:
                            self.logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, oco_order2.price))
                            p.order.fail_order()
                        elif oco_order2.vol == 0:
                            p.order.fail_order()
                        elif low <= oco_order2.price and open_price <= oco_order2.price:  # 寄り付きが安値の場合
                            # 最大volまで売却
                            order_price = open_price
                            (margin_cash, _) = asset.get_margin_cash(symbol)
                            order_vol = entry_strategy.get_order_vol(margin_cash, idx, order_price, p.last_exit_idx)
                            order_vol = order_vol * -1
                            p.entry_short(idx, candle_time, order_price, order_vol)
                        elif low <= oco_order2.price:
                            order_price = oco_order2.price
                            order_vol = oco_order2.vol
                            p.entry_short(idx, candle_time, oco_order2.price, order_vol)
                        else:
                            p.order.fail_order()
                        self.set_order_info(execution_order_info2, oco_order2)
                        # Open約定期間中のロスカット
                        if p.order.order_status == OrderStatus.EXECUTION:
                            losscut_price = order_price + (order_price * asset.get_losscut_ratio(symbol))
                            if high >= losscut_price:
                                oco_order2.order_type = OrderType.CLOSE_SHORT_STOP_MARKET
                                p.exit_short(idx, candle_time, losscut_price)
                                trade_performance = p.save_trade_performance(idx, PositionType.SHORT)
                                self.set_order_info(execution_order_info2, oco_order2)
            elif current_position == PositionType.LONG and p.order is not None:
                # 約定判定
                if p.order.order_type == OrderType.CLOSE_LONG_STOP_MARKET:  # 逆指値成行返売
                    if low <= p.order.price and open_price <= p.order.price:
                        p.exit_long(idx, candle_time, open_price)
                        trade_performance = p.save_trade_performance(idx, PositionType.LONG)
                    elif low <= p.order.price:
                        p.exit_long(idx, candle_time, p.order.price)
                        trade_performance = p.save_trade_performance(idx, PositionType.LONG)
                    else:
                        p.order.fail_order()
                elif p.order.order_type == OrderType.CLOSE_LONG_MARKET:  # 成行返売
                    p.exit_long(idx, candle_time, open_price)
                    trade_performance = p.save_trade_performance(idx, PositionType.LONG)
                elif p.order.order_type == OrderType.CLOSE_LONG_OCO:
                    # TODO:OCO CLOSE_LONG_STOP_LIMIT
                    # OCO1の判定
                    if p.order.oco_order1.order_type == OrderType.CLOSE_LONG_STOP_MARKET:
                        stop_market_price = p.order.oco_order1.price
                        # 逆指値の判定(始値)
                        if stop_market_price >= open_price:
                            p.exit_long(idx, candle_time, open_price)
                            trade_performance = p.save_trade_performance(idx, PositionType.LONG)
                        # 逆指値の判定
                        elif stop_market_price >= low:
                            p.exit_long(idx, candle_time, stop_market_price)
                            trade_performance = p.save_trade_performance(idx, PositionType.LONG)
                    # OCO2の判定
                    if p.order.oco_order2.order_type == OrderType.CLOSE_LONG_LIMIT:
                        limit_price = p.order.oco_order2.price
                        # 指値の判定(始値)
                        if limit_price <= open_price:
                            p.exit_long(idx, candle_time, limit_price)
                            trade_performance = p.save_trade_performance(idx, PositionType.LONG)
                        # 指値の判定
                        elif limit_price <= high:
                            p.exit_long(idx, candle_time, limit_price)
                            trade_performance = p.save_trade_performance(idx, PositionType.LONG)
                self.set_order_info(execution_order_info, p.order)
            elif current_position == PositionType.SHORT and p.order is not None:
                # 約定判定
                if p.order.order_type == OrderType.CLOSE_SHORT_STOP_MARKET:  # 逆指値成行返買
                    if high >= p.order.price and open_price >= p.order.price:
                        p.exit_short(idx, candle_time, open_price)
                        trade_performance = p.save_trade_performance(idx, PositionType.SHORT)
                    elif high >= p.order.price:
                        p.exit_short(idx, candle_time, p.order.price)
                        trade_performance = p.save_trade_performance(idx, PositionType.SHORT)
                    else:
                        p.order.fail_order()
                elif p.order.order_type == OrderType.CLOSE_SHORT_MARKET:  # 成行返買
                    p.exit_short(idx, candle_time, open_price)
                    trade_performance = p.save_trade_performance(idx, PositionType.SHORT)
                elif p.order.order_type == OrderType.CLOSE_SHORT_OCO:
                    # TODO:OCO CLOSE_SHORT_STOP_LIMIT
                    # OCO1
                    if p.order.oco_order1.order_type == OrderType.CLOSE_SHORT_STOP_MARKET:
                        stop_market_price = p.order.oco_order1.price
                        # 逆指値の判定(始値)
                        if stop_market_price <= open_price:
                            p.exit_short(idx, candle_time, open_price)
                            trade_performance = p.save_trade_performance(idx, PositionType.SHORT)
                        # 逆指値の判定(利確と損切りのどちらが先にトリガーとなっているかわからないため、損切りを優先して判定)
                        elif stop_market_price <= high:
                            p.exit_short(idx, candle_time, stop_market_price)
                            trade_performance = p.save_trade_performance(idx, PositionType.SHORT)
                    # OCO2
                    if p.order.oco_order2.order_type == OrderType.CLOSE_SHORT_LIMIT:
                        limit_price = p.order.oco_order2.price
                        # 指値の判定(始値)
                        if limit_price >= open_price:
                            p.exit_short(idx, candle_time, limit_price)
                            trade_performance = p.save_trade_performance(idx, PositionType.SHORT)
                            pass
                        # 指値の判定
                        elif limit_price >= low:
                            p.exit_short(idx, candle_time, limit_price)
                            trade_performance = p.save_trade_performance(idx, PositionType.SHORT)
                self.set_order_info(execution_order_info, p.order)

            # EntryしたバーでExitする場合
            if isinstance(exit_strategy, EndOfBar):
                current_position = p.get_position()
                # ポジションがある場合、大引けで成行クローズ
                if current_position == PositionType.LONG:
                    p.order.order_type = OrderType.CLOSE_LONG_MARKET
                    p.exit_long(idx, candle_time, close_price)
                    trade_performance = p.save_trade_performance(idx, PositionType.LONG)
                    self.set_order_info(execution_order_info2, p.order)
                elif current_position == PositionType.SHORT:
                    p.order.order_type = OrderType.CLOSE_SHORT_MARKET
                    p.exit_short(idx, candle_time, close_price)
                    trade_performance = p.save_trade_performance(idx, PositionType.SHORT)
                    self.set_order_info(execution_order_info2, p.order)

            # 注文はキャンドル一つ分だけ有効
            p.clear_order(idx)

            # 次のキャンドル用の注文作成
            current_position = p.get_position()
            if current_position == PositionType.NOTHING:
                long_order_type = entry_strategy.check_entry_long(idx, p.last_exit_idx)
                short_order_type = entry_strategy.check_entry_short(idx, p.last_exit_idx)
                if long_order_type == OrderType.OCO or short_order_type == OrderType.OCO:
                    # create OCO order stop market/stop market
                    (margin_cash, _) = asset.get_margin_cash(symbol)
                    (
                        stop_market_price_long,
                        vol_long) = entry_strategy.create_order_entry_long_stop_market_for_all_cash(
                        margin_cash, idx, p.last_exit_idx)
                    (stop_market_price_short, _) = entry_strategy.create_order_entry_short_stop_market_for_all_cash(
                        margin_cash, idx, p.last_exit_idx)
                    p.create_order_oco(idx, candle_time, stop_market_price_long, stop_market_price_short, vol_long)
                    self.set_order_info(order_info, p.order)
                elif long_order_type == OrderType.LIMIT_LONG:
                    # TODO:
                    (margin_cash, _) = asset.get_margin_cash(symbol)
                    (price, vol) = entry_strategy.create_order_open_long_limit_for_all_cash(margin_cash, idx,
                                                                                            p.last_exit_idx)
                    if vol > 0:
                        p.create_order_entry_long_limit(idx, candle_time, price, vol)
                        self.set_order_info(order_info, p.order)
                elif short_order_type == OrderType.LIMIT_SHORT:
                    # TODO:
                    (margin_cash, _) = asset.get_margin_cash(symbol)
                    (price, vol) = entry_strategy.create_order_open_short_limit_for_all_cash(margin_cash, idx,
                                                                                             p.last_exit_idx)
                    if vol < 0:
                        p.create_order_entry_short_limit(idx, candle_time, price, vol)
                        self.set_order_info(order_info, p.order)
                elif long_order_type == OrderType.STOP_MARKET_LONG:
                    # create stop market long
                    (margin_cash, _) = asset.get_margin_cash(symbol)
                    (price, vol) = entry_strategy.create_order_entry_long_stop_market_for_all_cash(margin_cash, idx,
                                                                                                   p.last_exit_idx)
                    if vol > 0:
                        p.create_order_entry_long_stop_market(idx, candle_time, price, vol)
                        self.set_order_info(order_info, p.order)
                elif short_order_type == OrderType.STOP_MARKET_SHORT:
                    # create stop market short
                    (margin_cash, _) = asset.get_margin_cash(symbol)
                    (price, vol) = entry_strategy.create_order_entry_short_stop_market_for_all_cash(margin_cash, idx,
                                                                                                    p.last_exit_idx)
                    if vol < 0:
                        p.create_order_entry_short_stop_market(idx, candle_time, price, vol)
                        self.set_order_info(order_info, p.order)
                elif long_order_type == OrderType.MARKET_LONG:
                    (margin_cash, _) = asset.get_margin_cash(symbol)
                    (price, vol) = entry_strategy.create_order_entry_long_market_for_all_cash(margin_cash, idx,
                                                                                              p.last_exit_idx)
                    if vol > 0:
                        p.create_order_entry_long_market(idx, candle_time, price, vol)
                        self.set_order_info(order_info, p.order)
                elif short_order_type == OrderType.MARKET_SHORT:
                    (margin_cash, _) = asset.get_margin_cash(symbol)
                    (price, vol) = entry_strategy.create_order_entry_short_market_for_all_cash(margin_cash, idx,
                                                                                               p.last_exit_idx)
                    if vol < 0:
                        p.create_order_entry_short_market(idx, candle_time, price, vol)
                        self.set_order_info(order_info, p.order)
            elif current_position == PositionType.LONG:
                exit_order_type = exit_strategy.check_exit_long(p.pos_price, p.pos_vol, idx, p.entry_idx)
                if exit_order_type == OrderType.CLOSE_LONG_STOP_MARKET:
                    # 逆指値成行返売注文
                    price = exit_strategy.create_order_exit_long_stop_market(idx, p.entry_idx)
                    p.create_order_exit_long_stop_market(idx, candle_time, price, p.pos_vol)
                    self.set_order_info(order_info, p.order)
                elif exit_order_type == OrderType.CLOSE_LONG_MARKET:
                    # 成行返売注文
                    price = exit_strategy.create_order_exit_long_market(idx, p.entry_idx)
                    p.create_order_exit_long_market(idx, candle_time, price, p.pos_vol)
                    self.set_order_info(order_info, p.order)
                elif exit_order_type == OrderType.CLOSE_LONG_OCO:
                    # OCO注文(指値,逆指値)
                    limit_price = exit_strategy.create_order_exit_long_limit(idx, p.entry_idx)
                    stop_market_price = exit_strategy.create_order_exit_long_stop_market(idx, p.entry_idx)
                    p.create_order_exit_long_oco(idx, candle_time, limit_price, stop_market_price, p.pos_vol)
                    self.set_order_info(order_info, p.order)
                    pass
                else:
                    pass  # 注文無し
            elif current_position == PositionType.SHORT:
                exit_order_type = exit_strategy.check_exit_short(p.pos_price, p.pos_vol, idx, p.entry_idx)
                if exit_order_type == OrderType.CLOSE_SHORT_STOP_MARKET:
                    # 逆指値成行返買注文
                    price = exit_strategy.create_order_exit_short_stop_market(idx, p.entry_idx)
                    p.create_order_exit_short_stop_market(idx, candle_time, price, p.pos_vol)
                    self.set_order_info(order_info, p.order)
                elif exit_order_type == OrderType.CLOSE_SHORT_MARKET:
                    # 成行返買注文
                    price = exit_strategy.create_order_exit_short_market(idx, p.entry_idx)
                    p.create_order_exit_short_market(idx, candle_time, price, p.pos_vol)
                    self.set_order_info(order_info, p.order)
                elif exit_order_type == OrderType.CLOSE_SHORT_OCO:
                    # OCO注文(指値,逆指値)
                    limit_price = exit_strategy.create_order_exit_short_limit(idx, p.entry_idx)
                    stop_market_price = exit_strategy.create_order_exit_short_stop_market(idx, p.entry_idx)
                    p.create_order_exit_short_oco(idx, candle_time, limit_price, stop_market_price, p.pos_vol)
                    self.set_order_info(order_info, p.order)
                else:
                    pass  # 注文無し
            # 1日の結果を出力
            close = 0
            if ohlcv.values['close'][idx] is None:
                close = 0
            else:
                close = ohlcv.values['close'][idx]
            history = self.dumper.make_history(
                ohlcv
                , entry_strategy.title
                , exit_strategy.title
                , idx
                , order_info
                , call_order_info
                , execution_order_info
                , execution_order_info2
                , p
                , asset
                , round(asset.cash + p.pos_vol * close, 2)
                , trade_performance
                , entry_strategy.get_indicators(idx, p.last_exit_idx)
                , entry_strategy.get_vol_indicators(idx, p.last_exit_idx)
                , exit_strategy.get_indicators(idx, p.entry_idx)
            )
            backtest_history.append(history)
        self.dumper.save_history(symbol, ohlcv.ashi, entry_strategy.title, exit_strategy.title, backtest_history)
        summary_msg = self.dumper.save_result(entry_strategy.title, exit_strategy.title, p.summary, ohlcv)
        self.logger.info(summary_msg)

    def set_order_info(self, info, order):
        info['create_time'] = order.create_time
        info['order_time'] = order.order_time
        info['exit_order_time'] = order.exit_order_time
        info['order_type'] = order.order_type
        info['order_status'] = order.order_status
        info['vol'] = order.vol
        info['price'] = order.price

#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import threading
from argparse import ArgumentParser
from donkatsu.mylogger import Logger
from donkatsu.market import Market
from donkatsu.asset import Asset
from donkatsu.dbaccess import DbAccess
from donkatsu.ohlcv import Ohlcv
from donkatsu.entry_strategy.range_breakout import RangeBreakout
from donkatsu.exit_strategy.newvalue import Newvalue

# from donkatsu.symbol.test import Symbol
# from donkatsu.symbol.bollingerband_newvalue import Symbol
# from donkatsu.symbol.topix17etf_nomura import Symbol
# from donkatsu.symbol.n225 import Symbol
from donkatsu.symbol.n225_topix import Symbol

s = Logger()
logger = s.myLogger()

# parameters
params = {}


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('--symbol', type=str, help='Absolute/relative path to input file')
    argparser.add_argument('--start_date', type=str, help='Date of backtest start')
    argparser.add_argument('--end_date', type=str, help='Date of backtest end')
    argparser.add_argument('--brute_force', action='store_true', help='breaking the code!')
    argparser.add_argument('--strategy', type=str, help='Choose Strategy!')
    argparser.add_argument('--ashi', type=str, help='ASHI!')
    args = argparser.parse_args()
    return args


def backtest_run(symbol
                 , ashi
                 , start_date
                 , end_date
                 , begin_time
                 , end_time
                 , atr_span_1d
                 , xfl
                 , xfs
                 , initial_cash
                 , leverage
                 , losscut_ratio
                 ):
    try:
        asset = Asset(symbol, initial_cash, leverage, losscut_ratio)
        ohlcv = Ohlcv(symbol, ashi, start_date, end_date)
        entry_title = f"RangeBreakout[{begin_time},{end_time}][{atr_span_1d:.0f},{xfl:.2f},{xfs:.2f}]"
        exit_title = "NewValue"
        entry_strategy = RangeBreakout(entry_title, ohlcv, begin_time, end_time, atr_span_1d, xfl, xfs)
        exit_strategy = Newvalue(exit_title, ohlcv)
        Market().simulator_run(ohlcv, entry_strategy, exit_strategy, asset)
    except Exception as err:
        print(err)


def bruteforce_backtest_open(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio):
    pass


def backtest(symbol, ashi, start_date, end_date, brute_force=False, long_flg=False, short_flg=False):
    logger.info("backtest start")
    logger.info(
        f"parameter symbol={symbol}, ashi={ashi}, start_date={start_date}, end_date={end_date}, brute_force={brute_force}")
    # trade_fee = 0.0
    initial_cash = 1000000
    leverage = 3.0
    losscut_ratio = 0.03
    if brute_force:
        # bruteforce_backtest_open(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio)
        pass
    else:
        # デフォルトのパラメータ
        begin_time = "084500"
        end_time = "100000"
        atr_span_1d = 10
        xfl = 1.0
        xfs = 1.0
        # symbolごとのparameter
        backtest_run(symbol
                     , ashi
                     , start_date
                     , end_date
                     , begin_time
                     , end_time
                     , atr_span_1d
                     , xfl
                     , xfs
                     , initial_cash
                     , leverage
                     , losscut_ratio
                     )
    logger.info("backtest end")


if __name__ == '__main__':
    s = Logger()
    args = get_option()
    if args.brute_force:
        brute_force = True
    else:
        brute_force = False
    if args.start_date is None:
        start_date = (datetime.today() - relativedelta(months=3)).strftime('%Y-%m-%d')  # 今日の3か月前
    else:
        start_date = args.start_date
    if args.ashi is None:
        ashi = '1d'
    else:
        ashi = args.ashi
    if args.symbol is None:
        symbols = Symbol.symbols
    else:
        symbols = args.symbol.split(',')
    thread_pool = list()
    for s in symbols:
        if args.end_date is None:
            try:
                dba = DbAccess()
                rs_enddate = dba.get_maxtime_from_ohlcv(s, ashi)
                if rs_enddate:
                    end_date = rs_enddate.strftime('%Y-%m-%d')
            except Exception as err:
                print(err)
        else:
            end_date = args.end_date
        thread_pool.append(threading.Thread(target=backtest, args=(s
                                                                   , ashi
                                                                   , start_date
                                                                   , end_date
                                                                   , brute_force
                                                                   )))
    thread_join_cnt = 0
    thread_pool_cnt = len(thread_pool)
    split_num = (thread_pool_cnt / 16) + 1
    thread_pools = list(np.array_split(thread_pool, split_num))
    for p in thread_pools:
        for t in p:
            t.start()
        for t in p:
            t.join()
            thread_join_cnt += 1
            logger.info("*** thread join[%d]/[%d] ***" % (thread_join_cnt, thread_pool_cnt))

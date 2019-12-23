#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import numpy as np
import threading
from argparse import ArgumentParser
from donkatsu.mylogger import Logger
from donkatsu.market import Market
from donkatsu.asset import Asset
from donkatsu.dbaccess import DbAccess
from donkatsu.ohlcv import Ohlcv
from donkatsu.entry_strategy.everyone_loves_friday import EveryoneLovesFriday
from donkatsu.exit_strategy.newvalue import Newvalue

from donkatsu.symbol.test import Symbol

# from donkatsu.symbol.n225 import Symbol
# from donkatsu.symbol.n225_topix import Symbol

s = Logger()
logger = s.myLogger()

# parameters
params = {
    # "^N225"    :[   21,  70,   3, 10,  6,  0.5,  1,  3,  2,  0.05 ]
    # ,"6753.T"   :[  60, 14,  0.4, 60, 14,  0.4,  1,  3,  2,  0.05 ]
    # ,"N225minif":[ 120, 14,  0.2,120, 14,  0.2,  1,  3,  3,  0.2  ]
    # ,"USDJPY"   :[ 120, 14,  0.2,120, 14,  0.2,  1,  3,  3,  0.2  ]
}


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('--symbol', type=str, help='symbol')
    argparser.add_argument('--start_date', type=str, help='Date of backtest start')
    argparser.add_argument('--end_date', type=str, help='Date of backtest end')
    argparser.add_argument('--brute_force', action='store_true', help='breaking the code!')
    argparser.add_argument('--ashi', type=str, help='ASHI!')
    args = argparser.parse_args()
    return args


def backtest_run(symbol
                 , ashi
                 , start_date
                 , end_date
                 , lookback
                 , long_entry_dayofweek
                 , short_entry_dayofweek
                 , initial_cash
                 , leverage
                 , losscut_ratio
                 ):
    try:
        asset = Asset(symbol, initial_cash, leverage, losscut_ratio)
        ohlcv = Ohlcv(symbol, ashi, start_date, end_date)
        long_entry_dayofweek_title = ",".join(map(str, long_entry_dayofweek))
        short_entry_dayofweek_title = ",".join(map(str, short_entry_dayofweek))
        open_title = f"EveryoneLovesFriday[{lookback:.0f}][{long_entry_dayofweek_title}][{short_entry_dayofweek_title}]"
        close_title = f"NewValue"
        entry_strategy = EveryoneLovesFriday(open_title, ohlcv, lookback, long_entry_dayofweek, short_entry_dayofweek)
        exit_strategy = Newvalue(close_title, ohlcv)
        Market().simulator_run(ohlcv, entry_strategy, exit_strategy, asset)
    except Exception as err:
        logger.error('error dayo. {0}'.format(err))


def bruteforce_backtest_open(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio, long_flg=True,
                             short_flg=True):
    pass


def bruteforce_backtest_close(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio, long_flg=True,
                              short_flg=False):
    pass


def backtest(symbol, ashi, start_date, end_date, brute_force=False):
    logger.info("backtest start")
    logger.info(
        f"parameter symbol={symbol}, ashi={ashi}, start_date={start_date}, end_date={end_date}, brute_force={brute_force}")
    # trade_fee = 0.0
    initial_cash = 1000000
    leverage = 3.0
    losscut_ratio = 0.03

    if brute_force:
        # bruteforce_backtest_open(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio)
        # bruteforce_backtest_close(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio, True, False)  # long
        # bruteforce_backtest_close(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio, False, True)  # short
        pass
    else:
        # デフォルトのパラメータ
        # ENTRY
        lookback = 25
        long_entry_dayofweek = [4]
        short_entry_dayofweek = [4]
        # symbolごとのparameter
        if symbol in params:
            lookback = params[symbol][0]
            long_entry_dayofweek = params[symbol][1]
            short_entry_dayofweek = params[symbol][2]
        backtest_run(symbol
                     , ashi
                     , start_date
                     , end_date
                     , lookback
                     , long_entry_dayofweek
                     , short_entry_dayofweek
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
        symbols = (args.symbol).split(',')
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
            print(s)
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

#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
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
from donkatsu.technical_indicator.average_directional_index import AverageDirectionalIndex
from donkatsu.entry_strategy.breakout_with_a_twist import BreakoutWithTwist
from donkatsu.exit_strategy.timed import Timed

#from donkatsu.symbol.test import Symbol
from donkatsu.symbol.topix17etf.topix17etf_nomura import Symbol
#from donkatsu.symbol.n225 import Symbol
#from donkatsu.symbol.n225_topix import Symbol
#from donkatsu.symbol.breakout_twist_timed_optimisation500 import Symbol

s = Logger()
logger = s.myLogger()

#parameters
params = {
            "^N225"    :[  10, 24,  0.3, 10,  6,  0.5,  1,  3,  2,  0.05 ]
            #,"6753.T"   :[  60, 14,  0.4, 60, 14,  0.4,  1,  3,  2,  0.05 ]
            ,"N225minif":[ 120, 14,  0.2,120, 14,  0.2,  1,  3,  3,  0.2  ]
            ,"USDJPY"   :[ 120, 14,  0.2,120, 14,  0.2,  1,  3,  3,  0.2  ]
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

def backtest_open_breakout_twist_close_timed(symbol
                                                , ashi
                                                , start_date
                                                , end_date
                                                , long_lookback_span
                                                , long_adx_span
                                                , long_adx_value
                                                , short_lookback_span
                                                , short_adx_span
                                                , short_adx_value
                                                , timed_method
                                                , num_of_bars_long
                                                , num_of_bars_short
                                                , close_losscut_ratio
                                                , initial_cash
                                                , leverage
                                                , losscut_ratio
                                                ):
    try:
        asset = Asset(symbol, initial_cash, leverage, losscut_ratio)
        ohlcv = Ohlcv(symbol, ashi, start_date, end_date)
        long_adx = AverageDirectionalIndex(ohlcv, long_adx_span)
        short_adx = AverageDirectionalIndex(ohlcv, short_adx_span)
        open_title = f"BreakoutTwist[{long_lookback_span:.0f},{long_adx_span:.0f},{long_adx_value:.2f}][{short_lookback_span:.0f},{short_adx_span:.0f},{short_adx_value:.2f}]"
        close_title = f"Timed[{timed_method}][{num_of_bars_long:.0f}][{num_of_bars_short:.0f}][{close_losscut_ratio:.2f}]"
        open_strategy = BreakoutWithTwist(open_title, ohlcv, long_lookback_span, long_adx_value, long_adx, short_lookback_span, short_adx_value, short_adx)
        close_strategy = Timed(close_title, ohlcv, timed_method, num_of_bars_long, num_of_bars_short, close_losscut_ratio)
        Market().simulator_run(ohlcv, open_strategy, close_strategy, asset) 
    except Exception as err:
        logger.error('error dayo. {0}'.format(err))

def bruteforce_backtest_open(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio, long_flg, short_flg):
    long_lookback_span  = 0 # 10 - 240
    long_adx_span       = 1 # 2 - 30
    long_adx_value      = 0 # 0.10 - 1.00
    short_lookback_span = 0
    short_adx_span      = 1
    short_adx_value     = 0
    timed_method        = 1
    num_of_bars_long    = 3
    num_of_bars_short   = 3
    close_losscut_ratio = 0.05

    if long_flg:
        for long_lookback_span in range(10, 240, 20):
            for long_adx_span in range(2, 30, 2):
                for long_adx_value in np.arange(0.1, 1.0, 0.2):
                    backtest_open_breakout_twist_close_timed(symbol , ashi , start_date , end_date , long_lookback_span , long_adx_span , long_adx_value , short_lookback_span , short_adx_span , short_adx_value , timed_method , num_of_bars_long , num_of_bars_short , close_losscut_ratio , initial_cash , leverage , losscut_ratio)
    if short_flg:
        for short_lookback_span in range(10, 240, 20):
            for short_adx_span in range(2, 30, 2):
                for short_adx_value in np.arange(0.1, 1.0, 0.2):
                    backtest_open_breakout_twist_close_timed(symbol , ashi , start_date , end_date , long_lookback_span , long_adx_span , long_adx_value , short_lookback_span , short_adx_span , short_adx_value , timed_method , num_of_bars_long , num_of_bars_short , close_losscut_ratio , initial_cash , leverage , losscut_ratio)


def bruteforce_backtest_close(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio):
    #デフォルトのパラメータ
    long_lookback_span  = 10
    long_adx_span       = 24 
    long_adx_value      = 0.3 
    #long_lookback_span  = 130
    #long_adx_span       = 26
    #long_adx_value      = 0.7 
    short_lookback_span = 10
    short_adx_span      = 6
    short_adx_value     = 0.50
    timed_method        = 1
    num_of_bars_long    = 3
    num_of_bars_short   = 3
    close_losscut_ratio = 0.03
    #symbolごとのparameter
    if symbol in params:
        long_lookback_span  = params[symbol][0]
        long_adx_span       = params[symbol][1]
        long_adx_value      = params[symbol][2]
        short_lookback_span = params[symbol][3]
        short_adx_span      = params[symbol][4]
        short_adx_value     = params[symbol][5]
        timed_method        = params[symbol][6]
        #num_of_bars_long    = params[symbol][7]
        #num_of_bars_short   = params[symbol][8]
        #close_losscut_ratio = params[symbol][9]
    for num_of_bars_long in range(1, 7, 1):
        for num_of_bars_short in range(1, 7, 1):
            for close_losscut_ratio in np.arange(0.01, 0.1, 0.01):
                backtest_open_breakout_twist_close_timed(symbol , ashi , start_date , end_date , long_lookback_span , long_adx_span , long_adx_value , short_lookback_span , short_adx_span , short_adx_value , timed_method , num_of_bars_long , num_of_bars_short , close_losscut_ratio , initial_cash , leverage , losscut_ratio)

def backtest(symbol, ashi, start_date, end_date, brute_force=False):
    logger.info("backtest start")
    logger.info(f"parameter symbol={symbol}, ashi={ashi}, start_date={start_date}, end_date={end_date}, brute_force={brute_force}")
    #trade_fee = 0.0
    initial_cash = 1000000
    leverage = 3.0
    losscut_ratio = 0.03

    if brute_force:
        #bruteforce_backtest_open(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio, True, False)
        bruteforce_backtest_open(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio, False, True)
        #bruteforce_backtest_close(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio)
    else:
        #デフォルトのパラメータ
        # long1
        long_lookback_span  = 10
        long_adx_span       = 24 
        long_adx_value      = 0.3 
        # long2
        #long_lookback_span  = 130
        #long_adx_span       = 26
        #long_adx_value      = 0.7 
        # long3
        #long_lookback_span  = 60
        #long_adx_span       = 14
        #long_adx_value      = 0.40
        #long_lookback_span  = 0
        #long_adx_span       = 1
        #long_adx_value      = 0
        # short1 
        short_lookback_span = 10 # [10,6,0.50]
        short_adx_span      = 6
        short_adx_value     = 0.50
        # short2 
        #short_lookback_span = 130 # [130,4,0.70]
        #short_adx_span      = 4
        #short_adx_value     = 0.70
        # short3
        #short_lookback_span = 60 # [60,14,0.40]
        #short_adx_span      = 14
        #short_adx_value     = 0.40
        #short_lookback_span = 0
        #short_adx_span      = 1
        #short_adx_value     = 0
        timed_method        = 1
        num_of_bars_long    = 3
        num_of_bars_short   = 3
        close_losscut_ratio = 0.03
        #symbolごとのparameter
        if symbol in params:
            long_lookback_span  = params[symbol][0]
            long_adx_span       = params[symbol][1]
            long_adx_value      = params[symbol][2]
            short_lookback_span = params[symbol][3]
            short_adx_span      = params[symbol][4]
            short_adx_value     = params[symbol][5]
            timed_method        = params[symbol][6]
            num_of_bars_long    = params[symbol][7]
            num_of_bars_short   = params[symbol][8]
            close_losscut_ratio = params[symbol][9]
        backtest_open_breakout_twist_close_timed(symbol
                                                    , ashi
                                                    , start_date
                                                    , end_date
                                                    , long_lookback_span
                                                    , long_adx_span
                                                    , long_adx_value
                                                    , short_lookback_span
                                                    , short_adx_span
                                                    , short_adx_value
                                                    , timed_method
                                                    , num_of_bars_long
                                                    , num_of_bars_short
                                                    , close_losscut_ratio
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
        start_date = (datetime.today() - relativedelta(months=3)).strftime('%Y-%m-%d') #今日の3か月前
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

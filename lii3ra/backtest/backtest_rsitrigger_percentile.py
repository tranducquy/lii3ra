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
from donkatsu.technical_indicator.relative_strength_index import RelativeStrengthIndex
from donkatsu.technical_indicator.exponentially_smoothed_movingaverage import ExponentiallySmoothedMovingAverage
from donkatsu.entry_strategy.rsi_trigger import RSITrigger
from donkatsu.exit_strategy.percentile import Percentile
from donkatsu.symbol.test import Symbol
#from donkatsu.symbol.n225 import Symbol
#from donkatsu.symbol.n225_topix import Symbol

s = Logger()
logger = s.myLogger()

#parameters
params = {
            # "^N225"    :[   21,  70,   3, 10,  6,  0.5,  1,  3,  2,  0.05 ]
            #,"6753.T"   :[  60, 14,  0.4, 60, 14,  0.4,  1,  3,  2,  0.05 ]
            #,"N225minif":[ 120, 14,  0.2,120, 14,  0.2,  1,  3,  3,  0.2  ]
            #,"USDJPY"   :[ 120, 14,  0.2,120, 14,  0.2,  1,  3,  3,  0.2  ]
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

def backtest_open_rsitrigger_close_percentile(symbol
                                                , ashi
                                                , start_date
                                                , end_date
                                                , rsi_span
                                                , rsi_threshold
                                                , ema_span
                                                , percentile_span_long
                                                , percentile_ratio_long
                                                , percentile_span_short
                                                , percentile_ratio_short
                                                , percentile_losscut_ratio
                                                , initial_cash
                                                , leverage
                                                , losscut_ratio
                                                ):
    try:
        asset = Asset(symbol, initial_cash, leverage, losscut_ratio)
        ohlcv = Ohlcv(symbol, ashi, start_date, end_date)
        rsi = RelativeStrengthIndex(ohlcv, rsi_span)
        ema = ExponentiallySmoothedMovingAverage(ohlcv, ema_span)
        open_title = f"RSITrigger[{rsi_span:.0f},{rsi_threshold:.0f},{ema_span:.0f}]"
        close_title = f"Percentile[{percentile_span_long:.0f},{percentile_ratio_long:.0f}][{percentile_span_short:.0f},{percentile_ratio_short:.0f}][{percentile_losscut_ratio:.2f}]"
        open_strategy = RSITrigger(open_title, ohlcv, rsi, rsi_threshold, ema)
        close_strategy = Percentile(close_title, ohlcv, percentile_span_long, percentile_ratio_long, percentile_span_short, percentile_ratio_short, percentile_losscut_ratio)
        Market().simulator_run(ohlcv, open_strategy, close_strategy, asset) 
    except Exception as err:
        logger.error('error dayo. {0}'.format(err))

def bruteforce_backtest_open(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio, long_flg=True, short_flg=True):
    #デフォルトのパラメータ
    # ENTRY
    rsi_span      =   5 # 2 - 30
    rsi_threshold =  80 # 10 - 90
    ema_span      =   5 # 2 - 30
    # EXIT
    percentile_span_long     =   5
    percentile_ratio_long    =  50
    percentile_span_short    =   5
    percentile_ratio_short   =  50
    percentile_losscut_ratio =   0.03

    for rsi_span in range(3, 30, 3):
        for rsi_threshold in range(10, 100, 10):
            for ema_span in range(3, 30, 3):
                backtest_open_rsitrigger_close_percentile(symbol, ashi, start_date, end_date, rsi_span, rsi_threshold, ema_span, percentile_span_long, percentile_ratio_long, percentile_span_short, percentile_ratio_short, percentile_losscut_ratio, initial_cash, leverage, losscut_ratio)

def bruteforce_backtest_close(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio, long_flg=True, short_flg=False):
    #デフォルトのパラメータ
    # ENTRY
    rsi_span      =  21 # 2 - 30
    rsi_threshold =  70 # 10 - 90
    ema_span      =   3 # 2 - 30
    # EXIT
    percentile_span_long     =   5 # 2 - 20
    percentile_ratio_long    =  50 # 10 - 90
    percentile_span_short    =   5 # 2 - 20
    percentile_ratio_short   =  50 # 10 - 90
    percentile_losscut_ratio =   0.03 # 0.01 - 0.10
    # long
    if long_flg:
        for percentile_span_long in range(2, 20, 1):
            for percentile_ratio_long in range(10, 100, 10):
                for percentile_losscut_ratio in np.arange(0.01, 0.09, 0.02):
                    backtest_open_rsitrigger_close_percentile(symbol, ashi, start_date, end_date, rsi_span, rsi_threshold, ema_span, percentile_span_long, percentile_ratio_long, percentile_span_short, percentile_ratio_short, percentile_losscut_ratio, initial_cash, leverage, losscut_ratio)
    # short
    if short_flg:
        for percentile_span_short in range(2, 20, 1):
            for percentile_ratio_short in range(10, 100, 10):
                for percentile_losscut_ratio in np.arange(0.01, 0.09, 0.02):
                    backtest_open_rsitrigger_close_percentile(symbol, ashi, start_date, end_date, rsi_span, rsi_threshold, ema_span, percentile_span_long, percentile_ratio_long, percentile_span_short, percentile_ratio_short, percentile_losscut_ratio, initial_cash, leverage, losscut_ratio)

def backtest(symbol, ashi, start_date, end_date, brute_force=False):
    logger.info("backtest start")
    logger.info(f"parameter symbol={symbol}, ashi={ashi}, start_date={start_date}, end_date={end_date}, brute_force={brute_force}")
    #trade_fee = 0.0
    initial_cash = 1000000
    leverage = 3.0
    losscut_ratio = 0.03

    if brute_force:
        #bruteforce_backtest_open(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio)
        bruteforce_backtest_close(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio, True, False) # long
        bruteforce_backtest_close(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio, False, True) # short
        pass
    else:
        #デフォルトのパラメータ
        # ENTRY
        rsi_span      =  21 
        rsi_threshold =  70
        ema_span      =   3
        # EXIT
        percentile_span_long     =   7
        percentile_ratio_long    =  80
        percentile_span_short    =   5
        percentile_ratio_short   =  40
        percentile_losscut_ratio =   0.03
        #symbolごとのparameter
        if symbol in params:
            rsi_span      = params[symbol][0]
            rsi_threshold = params[symbol][1]
            ema_span      = params[symbol][2]
            percentile_span_long     = params[symbol][3]
            percentile_ratio_long    = params[symbol][4]
            percentile_span_short    = params[symbol][3]
            percentile_ratio_short   = params[symbol][5]
            percentile_losscut_ratio = params[symbol][6]
        backtest_open_rsitrigger_close_percentile(symbol
                                                    , ashi
                                                    , start_date
                                                    , end_date
                                                    , rsi_span
                                                    , rsi_threshold
                                                    , ema_span
                                                    , percentile_span_long
                                                    , percentile_ratio_long
                                                    , percentile_span_short
                                                    , percentile_ratio_short
                                                    , percentile_losscut_ratio
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

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
from donkatsu.technical_indicator.exponentially_smoothed_movingaverage import ExponentiallySmoothedMovingAverage
from donkatsu.entry_strategy.ema_cross_with_a_twist import EMACrossWithTwist
from donkatsu.exit_strategy.percentile import Percentile

s = Logger()
logger = s.myLogger()

#parameters
params = { }

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
                    , fast_ema_span
                    , slow_ema_span
                    , price_threshold
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
        fast_ema = ExponentiallySmoothedMovingAverage(ohlcv, fast_ema_span)
        slow_ema = ExponentiallySmoothedMovingAverage(ohlcv, slow_ema_span)
        open_title = f"EMACrossWithTwist[{fast_ema_span:.0f},{slow_ema_span:.0f},{price_threshold:.2f}]"
        close_title = f"Percentile[{percentile_span_long:.0f},{percentile_ratio_long:.0f}][{percentile_span_short:.0f},{percentile_ratio_short:.0f}][{percentile_losscut_ratio:.2f}]"
        open_strategy = EMACrossWithTwist(open_title, ohlcv, fast_ema, slow_ema, price_threshold)
        close_strategy = Percentile(close_title, ohlcv, percentile_span_long, percentile_ratio_long, percentile_span_short, percentile_ratio_short, percentile_losscut_ratio)
        Market().simulator_run(ohlcv, open_strategy, close_strategy, asset) 
    except Exception as err:
        logger.error('error dayo. {0}'.format(err))

def bruteforce_open_breakout_sigma1_close_timed(symbol):
    pass

def backtest(symbol, ashi, start_date, end_date, brute_force=False, long_flg=False, short_flg=False):
    logger.info("backtest start")
    logger.info(f"parameter symbol={symbol}, ashi={ashi}, start_date={start_date}, end_date={end_date}, brute_force={brute_force}")
    #trade_fee = 0.0
    initial_cash = 1000000
    leverage = 3.0
    losscut_ratio = 0.03
    if brute_force:
        #bruteforce(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio, long_flg, short_flg)
        pass
    else:
        #デフォルトのパラメータ
        # Entry
        fast_ema_span   =  10
        slow_ema_span   =  20
        price_threshold = 790 #3%くらいかな
        # Exit
        percentile_span_long     =   7 # 2 - 20
        percentile_ratio_long    =  80 # 10 - 90
        percentile_span_short    =   5 # 2 - 20
        percentile_ratio_short   =  40 # 10 - 90
        percentile_losscut_ratio =   0.03 # 0.01 - 0.10
        #symbolごとのparameter
        if symbol in params:
            fast_ema_span            = params[symbol][0]
            slow_ema_span            = params[symbol][1]
            price_threshold          = params[symbol][2]
            percentile_span_long     = params[symbol][3]
            percentile_ratio_long    = params[symbol][4]
            percentile_span_short    = params[symbol][5]
            percentile_ratio_short   = params[symbol][6]
            percentile_losscut_ratio = params[symbol][7]
        backtest_run(symbol
                        , ashi
                        , start_date
                        , end_date
                        , fast_ema_span
                        , slow_ema_span
                        , price_threshold
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
    if args.symbol is None:
        symbol = "USDJPY"
    else:
        symbol = args.symbol
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
    if args.end_date is None:
        try:
            dba = DbAccess()
            rs_enddate = dba.get_maxtime_from_ohlcv(symbol, ashi)
            if rs_enddate:
                end_date = rs_enddate.strftime('%Y-%m-%d')
        except Exception as err:
            print(err)
            exit()
    else:
        end_date = args.end_date
    symbols = symbol.split(",")
    for s in symbols:
        print(s)
        backtest(s, ashi, start_date, end_date, brute_force, True, True)


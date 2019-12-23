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
from donkatsu.exit_strategy.getting_is_good import GettingIsGood

from donkatsu.symbol.n225_topix import Symbol

s = Logger()
logger = s.myLogger()

def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('--symbol', type=str, help='symbol')
    argparser.add_argument('--start_date', type=str, help='Date of backtest start')
    argparser.add_argument('--end_date', type=str, help='Date of backtest end')
    argparser.add_argument('--brute_force', action='store_true', help='breaking the code!')
    argparser.add_argument('--ashi', type=str, help='ASHI!')
    args = argparser.parse_args()
    return args

def backtest_open_breakout_twist_close_gettinggood(symbol
                                                , ashi
                                                , start_date
                                                , end_date
                                                , long_span
                                                , long_adx_value
                                                , short_span
                                                , short_adx_value
                                                , num_of_bars_long
                                                , num_of_bars_short
                                                , close_losscut_ratio
                                                , initial_cash
                                                , leverage
                                                , losscut_ratio
                                                ):
    asset = Asset(symbol, initial_cash, leverage, losscut_ratio)
    ohlcv = Ohlcv(symbol, ashi, start_date, end_date)
    long_adx = AverageDirectionalIndex(ohlcv, long_span)
    short_adx = AverageDirectionalIndex(ohlcv, short_span)
    open_title = f"BreakoutTwist[{long_span:.0f},{long_adx_value:.0f}][{short_span:.0f},{short_adx_value:.0f}]"
    close_title = f"GettingIsGood[{num_of_bars_long:.0f}][{num_of_bars_short:.0f}][{close_losscut_ratio:.2f}]"
    open_strategy = BreakoutWithTwist(open_title, ohlcv, long_span, long_adx_value, long_adx, short_span, short_adx_value, short_adx)
    close_strategy = GettingIsGood(close_title, ohlcv, num_of_bars_long, num_of_bars_short, close_losscut_ratio)
    Market().simulator_run(ohlcv, open_strategy, close_strategy, asset) 

def bruteforce_open_breakout_sigma1_close_timed(symbol):
    pass

def backtest(symbol, ashi, start_date, end_date, brute_force=False, long_flg=False, short_flg=False):
    logger.info("backtest start")
    logger.info(f"parameter symbol={symbol}, ashi={ashi}, start_date={start_date}, end_date={end_date}, brute_force={brute_force}")
    #trade_fee = 0.0
    initial_cash = 1000000
    leverage = 3.0
    losscut_ratio = 0.03
    #parameters
    params = {
                "1321.T":[ 
                     3
                    ,0.6
                    ,5
                    ,7
                    ,1.1
                    ,3
                    ,2
                ]
                ,"1356.T":[
                     4
                    ,1.4
                    ,5
                    ,13
                    ,1.2
                    ,2
                    ,2
                ]
                ,"1357.T":[
                     4
                    ,2.4
                    ,5
                    ,4
                    ,0.1
                    ,2
                    ,3
                ]
                ,"1568.T":[ 
                     12
                    ,2.0
                    ,5
                    ,4
                    ,1.5
                    ,2
                    ,2
                ]
                ,"1570.T":[ 
                     120
                    ,20
                    ,120
                    ,20
                    ,2
                    ,2
                    ,0.1
                ]
                ,"5801.T":[
                     4
                    ,0.6
                    ,5
                    ,0
                    ,0
                    #,4
                    #,2.2
                    ,2
                    ,2
                ]
                ,"5631.T":[
                     5
                    ,1.9
                    ,5
                    ,3
                    ,1.8
                    #,4
                    #,2.2
                    ,2
                    ,2
                ]
                ,"6141.T":[
                     4
                    ,1.0
                    ,5
                    ,5
                    ,1.7
                    ,2
                    ,2
                ]
                ,"6753.T":[
                     120
                    ,20
                    ,120
                    ,20
                    ,2
                    ,2
                    ,0.05
                ]
                ,"6981.T":[
                     3
                    ,0.4
                    ,5
                    ,3
                    ,2.4
                    ,2
                    ,2
                ]
                ,"9104.T":[
                     18
                    ,0.9
                    ,5
                    ,0
                    ,0
                    #,2
                    #,1.1
                    ,2
                    ,2
                ]
                ,"9107.T":[
                     6
                    ,0.4
                    ,5
                    ,21
                    ,1.9
                    ,2
                    ,2
                ]
                ,"^N225":[
                     120
                    ,20
                    ,120
                    ,20
                    ,3
                    ,3
                    ,0.2
                ]
                ,"N225mini":[
                     10
                    ,0.9
                    ,5
                    ,3
                    ,1.4
                    ,2
                    ,2
                ]
                #,"USDJPY":[ 5 ,0.9 ,5 ,5 ,2.0 ,2 ,2 ]
                }
    if brute_force:
        #bruteforce(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio, long_flg, short_flg)
        pass
    else:
        #デフォルトのパラメータ
        long_span           = 120
        long_adx_value      = 20
        short_span          = 120
        short_adx_value     = 20
        num_of_bars_long    = 2
        num_of_bars_short   = 2
        close_losscut_ratio = 0.03
        #symbolごとのparameter
        if symbol in params:
            long_span           = params[symbol][0]
            long_adx_value      = params[symbol][1]
            short_span          = params[symbol][2]
            short_adx_value     = params[symbol][3]
            num_of_bars_long    = params[symbol][4]
            num_of_bars_short   = params[symbol][5]
            close_losscut_ratio = params[symbol][6]
        backtest_open_breakout_twist_close_gettinggood(symbol
                                                    , ashi
                                                    , start_date
                                                    , end_date
                                                    , long_span
                                                    , long_adx_value
                                                    , short_span
                                                    , short_adx_value
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
    symbols = Symbol.symbols
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
        backtest(s, ashi, start_date, end_date, brute_force, True, True)


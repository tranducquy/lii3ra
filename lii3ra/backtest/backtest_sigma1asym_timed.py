#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import numpy as np
import threading
from argparse import ArgumentParser
import mylogger 
from market import Market
from asset import Asset
from dbaccess import DbAccess
from ohlcv import Ohlcv
from donkatsu.technical_indicator.bollingerband import Bollingerband
from donkatsu.technical_indicator.simple_movingaverage import SimpleMovingAverage
from donkatsu.entry_strategy.breakout_bb_sigma1_asym import BreakoutBBSigma1Asym
from donkatsu.exit_strategy.timed import Timed

s = mylogger.Logger()
logger = s.myLogger()

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

def backtest_open_breakout_sigma1_close_timed(symbol
                                                , ashi
                                                , start_date
                                                , end_date
                                                , long_sma_span
                                                , long_sigma1_ratio
                                                , vol_sma_span
                                                , short_sma_span
                                                , short_sigma1_ratio
                                                , timed_method
                                                , num_of_bars_long
                                                , num_of_bars_short
                                                , initial_cash
                                                , leverage
                                                , losscut_ratio
                                                ):
    asset = Asset(symbol, initial_cash, leverage, losscut_ratio)
    ohlcv = Ohlcv(symbol, ashi, start_date, end_date)
    long_bb = Bollingerband(ohlcv, long_sma_span, long_sigma1_ratio)
    short_bb = Bollingerband(ohlcv, short_sma_span, short_sigma1_ratio)
    vol_sma = SimpleMovingAverage(ohlcv, long_sma_span, vol_sma_span)
    open_title = f"BreakOutSigma1[{long_sma_span:.0f},{long_sigma1_ratio:.1f}][{short_sma_span:.0f},{short_sigma1_ratio:.1f}]"
    close_title = f"Timed[{timed_method}][{num_of_bars_long:.0f}][{num_of_bars_short:.0f}]"
    open_strategy = BreakoutBBSigma1Asym(open_title, ohlcv, long_bb, short_bb, vol_sma)
    close_strategy = Timed(close_title, ohlcv, timed_method, num_of_bars_long, num_of_bars_short)
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
                "1570.T":[ 
                     3
                    ,0.6
                    ,5
                    ,7
                    ,1.1
                    ,4
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
                ,"1357.T":[
                     4
                    ,2.4
                    ,5
                    ,4
                    ,0.1
                    ,2
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
                    ,4
                    ,2
                ]
                ,"6753.T":[
                     4
                    ,0.8
                    ,5
                    ,8
                    ,1.4
                    ,3
                    ,2
                ]
                ,"6981.T":[
                     3
                    ,0.4
                    ,5
                    ,3
                    ,2.4
                    ,3
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
                    ,3
                    ,0
                ]
                ,"9107.T":[
                     6
                    ,0.4
                    ,5
                    ,21
                    ,1.9
                    ,4
                    ,4
                ]
                ,"^N225":[
                     10
                    ,0.9
                    ,5
                    ,3
                    ,1.4
                    ,3
                    ,2
                ]
                ,"N225mini":[
                     10
                    ,0.9
                    ,5
                    ,3
                    ,1.4
                    ,3
                    ,2
                ]
                ,"USDJPY":[
                     5
                    ,0.9
                    ,5
                    ,5
                    ,2.0
                    ,2
                    ,2
                ]
                }
    if brute_force:
        #bruteforce(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio, long_flg, short_flg)
        pass
    else:
        #デフォルトのパラメータ
        long_sma_span = 3
        long_sigma1_ratio = 1.0
        vol_sma_span = 5
        short_sma_span = 3
        short_sigma1_ratio = 1.0
        timed_method = 1
        num_of_bars_long = 2
        num_of_bars_short = 2
        #symbolごとのparameter
        if symbol in params:
            long_sma_span = params[symbol][0]
            long_sigma1_ratio = params[symbol][1]
            vol_sma_span = params[symbol][2]
            short_sma_span = params[symbol][3]
            short_sigma1_ratio = params[symbol][4]
            num_of_bars_long = params[symbol][5]
            num_of_bars_short = params[symbol][6]
        backtest_open_breakout_sigma1_close_timed(symbol
                                                    , ashi
                                                    , start_date
                                                    , end_date
                                                    , long_sma_span
                                                    , long_sigma1_ratio
                                                    , vol_sma_span
                                                    , short_sma_span
                                                    , short_sigma1_ratio
                                                    , timed_method
                                                    , num_of_bars_long
                                                    , num_of_bars_short
                                                    , initial_cash
                                                    , leverage
                                                    , losscut_ratio
                                                    )
    logger.info("backtest end")

if __name__ == '__main__':
    s = mylogger.Logger()
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


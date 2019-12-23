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
from donkatsu.technical_indicator.bollingerband import Bollingerband
from donkatsu.technical_indicator.simple_movingaverage import SimpleMovingAverage
from donkatsu.entry_strategy.breakout_bb_sigma1 import BreakoutBBSigma1
from donkatsu.exit_strategy.newvalue import Newvalue

s = Logger()
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

def backtest_open_breakout_bbsigma1_close_newvalue(symbol
                                                    , ashi
                                                    , start_date
                                                    , end_date
                                                    , sma_duration
                                                    , vol_sma_duration
                                                    , sigma1_ratio
                                                    , candle_count
                                                    , initial_cash
                                                    , leverage
                                                    , losscut_ratio
                                                    ):
    asset = Asset(symbol, initial_cash, leverage, losscut_ratio)
    ohlcv = Ohlcv(symbol, ashi, start_date, end_date)
    bb = Bollingerband(ohlcv, sma_duration, sigma1_ratio)
    vol_sma = SimpleMovingAverage(ohlcv, sma_duration, vol_sma_duration)
    open_title = f"BreakOutBB1.SMA{sma_duration:.0f}SD{sigma1_ratio:.1f}"
    close_title = f"NewValue{candle_count:.0f}"
    open_strategy = BreakoutBBSigma1(open_title, ohlcv, bb, vol_sma)
    close_strategy = Newvalue(close_title, ohlcv)
    Market().simulator_run(ohlcv, open_strategy, close_strategy, asset) 

def bruteforce_open_backtest_breakout_bbsigma1_close_newvalue(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio):
    #単純移動平均2-25
    min_sma_duration = 2
    max_sma_duration = 25
    #標準偏差0.1-2.5
    min_sigma1_duration = 0.1
    max_sigma1_duration = 2.5
    sigma1_band = 0.1
    #出来高の平均
    vol_sma = 5
    candle_count = 1
    for bollinger_sma in range(min_sma_duration, max_sma_duration):
        thread_pool = list()
        for sigma1_ratio in np.arange(min_sigma1_duration, max_sigma1_duration, sigma1_band):
            #スレッド作成
            thread_pool.append(threading.Thread(target=backtest_open_breakout_bbsigma1_close_newvalue, args=(symbol
                                                                                        , ashi
                                                                                        , start_date
                                                                                        , end_date
                                                                                        , bollinger_sma
                                                                                        , vol_sma
                                                                                        , sigma1_ratio
                                                                                        , candle_count
                                                                                        , initial_cash
                                                                                        , leverage
                                                                                        , losscut_ratio
                                                                                        )))
        thread_join_cnt = 0
        thread_pool_cnt = len(thread_pool)
        #スレッド実行
        for t in thread_pool:
            t.start()
        #スレッド終了まで待機
        for t in thread_pool:
            t.join()
            thread_join_cnt += 1
            logger.info("*** thread join[%d]/[%d] ***" % (thread_join_cnt, thread_pool_cnt))
        thread_pool.clear()
    logger.info("bruteforce_bollingerband_dailytrail done symbol[%s]" % (symbol))

def backtest(symbol, ashi, start_date, end_date, brute_force=False):
    logger.info("backtest start")
    logger.info(f"parameter symbol={symbol}, ashi={ashi}, start_date={start_date}, end_date={end_date}, brute_force={brute_force}")
    #trade_fee = 0.0
    initial_cash = 1000000
    leverage = 3.0
    losscut_ratio = 0.03
    #parameters
    params = {
                 'N225mini': [2, 2.3, 1, 5]
                # 'N225mini': [7, 2.4, 1, 5]
                ,'1321.T': [2, 2.3, 1, 5]
                ,'1356.T': [4, 1.4, 1, 5]
                ,'1357.T': [8, 1.1, 1, 5]
                ,'1568.T': [3, 1.6, 1, 5]
                ,'1570.T': [4, 0.4, 1, 5]
                ,'1571.T': [2, 2.3, 1, 5]
                ,'6141.T': [4, 1.5, 1, 5]
                ,'6753.T': [14, 0.4, 1, 5]
                ,'9104.T': [18, 1.0, 1, 5]
                ,'9107.T': [13, 0.9, 1, 5]
                ,'^N225': [3, 1.3, 1, 5]
                }

    if brute_force:
        bruteforce_open_backtest_breakout_bbsigma1_close_newvalue(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio)
    else:
        #デフォルトのパラメータ
        sma_duration = 3
        sigma1_ratio = 1.0
        candle_count = 1
        vol_sma_duration = 5
        #symbolごとのparameter
        if symbol in params:
            sma_duration = params[symbol][0]
            sigma1_ratio = params[symbol][1]
            candle_count = params[symbol][2]
            vol_sma_duration = params[symbol][3]
        backtest_open_breakout_bbsigma1_close_newvalue(symbol, ashi, start_date, end_date, sma_duration, vol_sma_duration, sigma1_ratio, candle_count, initial_cash, leverage, losscut_ratio)
    logger.info("backtest end")

if __name__ == '__main__':
    s = Logger()
    args = get_option()
    if args.symbol is None:
        symbol = ["USDJPY"]
    else:
        symbol = args.symbol.split(',')
    if args.brute_force:
        brute_force = True
    else:
        brute_force = False
    if args.start_date is None:
        start_date = (datetime.today() - relativedelta(months=3)).strftime('%Y-%m-%d') #今日の3か月前
    else:
        start_date = args.start_date
    if args.ashi is None:
        #ashi = '1d'
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
    for s in symbol:
        backtest(s, ashi, start_date, end_date, brute_force)
    #backtest(symbol, ashi, start_date, end_date, True)

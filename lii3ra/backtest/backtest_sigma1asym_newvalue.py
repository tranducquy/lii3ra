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
from donkatsu.entry_strategy.breakout_bb_sigma1_asym import BreakoutBBSigma1Asym
from donkatsu.exit_strategy.newvalue import Newvalue

#from donkatsu.symbol.test import Symbol
from donkatsu.symbol.bollingerband_newvalue import Symbol
#from donkatsu.symbol.topix17etf_nomura import Symbol
#from donkatsu.symbol.n225 import Symbol
#from donkatsu.symbol.n225_topix import Symbol

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

def backtest_open_breakout_bbsigma1_close_newvalue_asym(symbol
                                                        , ashi
                                                        , start_date
                                                        , end_date
                                                        , long_sma_span
                                                        , long_sigma1_ratio
                                                        , vol_sma_span
                                                        , short_sma_span
                                                        , short_sigma1_ratio
                                                        , initial_cash
                                                        , leverage
                                                        , losscut_ratio
                                                        ):
    try:
        asset = Asset(symbol, initial_cash, leverage, losscut_ratio)
        ohlcv = Ohlcv(symbol, ashi, start_date, end_date)
        long_bb = Bollingerband(ohlcv, long_sma_span, long_sigma1_ratio)
        short_bb = Bollingerband(ohlcv, short_sma_span, short_sigma1_ratio)
        vol_sma = SimpleMovingAverage(ohlcv, long_sma_span, vol_sma_span)
        open_title = f"BreakOutSigma1[{long_sma_span:.0f},{long_sigma1_ratio:.1f}][{short_sma_span:.0f},{short_sigma1_ratio:.1f}]"
        close_title = f"NewValue"
        open_strategy = BreakoutBBSigma1Asym(open_title, ohlcv, long_bb, short_bb, vol_sma)
        close_strategy = Newvalue(close_title, ohlcv)
        Market().simulator_run(ohlcv, open_strategy, close_strategy, asset) 
    except Exception as err:
        print(err)

def bruteforce_open_backtest_breakout_bbsigma1_close_newvalue(symbol
                                                                , ashi
                                                                , start_date
                                                                , end_date
                                                                , initial_cash
                                                                , leverage
                                                                , losscut_ratio
                                                                , long_flg
                                                                , short_flg
                                                                ):
    #単純移動平均2-25
    min_sma_span = 2
    max_sma_span = 25
    #標準偏差0.1-2.5
    min_sigma1_span = 0.1
    max_sigma1_span = 2.5
    sigma1_band = 0.1
    #出来高の平均
    vol_sma = 5
    if long_flg:
        for long_sma in range(min_sma_span, max_sma_span):
            thread_pool = list()
            for long_sigma1_ratio in np.arange(min_sigma1_span, max_sigma1_span, sigma1_band):
                short_sma = 0
                short_sigma1_ratio = 0.0
                #スレッド作成
                thread_pool.append(threading.Thread(target=backtest_open_breakout_bbsigma1_close_newvalue_asym, args=(symbol
                                                                                        , ashi
                                                                                        , start_date
                                                                                        , end_date
                                                                                        , long_sma
                                                                                        , long_sigma1_ratio
                                                                                        , vol_sma
                                                                                        , short_sma
                                                                                        , short_sigma1_ratio
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
    if short_flg:
        for short_sma in range(min_sma_span, max_sma_span):
            thread_pool = list()
            for short_sigma1_ratio in np.arange(min_sigma1_span, max_sigma1_span, sigma1_band):
                long_sma = 0
                long_sigma1_ratio = 0.0
                #スレッド作成
                thread_pool.append(threading.Thread(target=backtest_open_breakout_bbsigma1_close_newvalue_asym, args=(symbol
                                                                                        , ashi
                                                                                        , start_date
                                                                                        , end_date
                                                                                        , long_sma
                                                                                        , long_sigma1_ratio
                                                                                        , vol_sma
                                                                                        , short_sma
                                                                                        , short_sigma1_ratio
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

def backtest(symbol, ashi, start_date, end_date, brute_force=False, long_flg=False, short_flg=False):
    logger.info("backtest start")
    logger.info(f"parameter symbol={symbol}, ashi={ashi}, start_date={start_date}, end_date={end_date}, brute_force={brute_force}")
    #trade_fee = 0.0
    initial_cash = 1000000
    leverage = 3.0
    losscut_ratio = 0.03
    #parameters
    params = {
                 "1570.T":[  3,  0.6,  5,  7,  1.1 ]
                ,"1568.T":[ 12,  2.0,  5,  4,  1.5 ]
                ,"1357.T":[  4,  2.4,  5,  4,  0.1 ]
                ,"1356.T":[  4,  1.4,  5, 13,  1.2 ]
                ,"5801.T":[  4,  0.6,  5,  0,  0   ] #,4 #,2.2 ]
                ,"5631.T":[  5,  1.9,  5,  3,  1.8 ] #,4 #,2.2 ]
                ,"6141.T":[  4,  1.0,  5,  5,  1.7 ]
                ,"6753.T":[  4,  0.8,  5,  8,  1.4 ]
                ,"6981.T":[  3,  0.4,  5,  3,  2.4 ]
                ,"9104.T":[ 18,  0.9,  5,  0,  0   ] #,2 #,1.1 ]
                ,"9107.T":[  6,  0.4,  5, 21,  1.9 ]
                ,"^N225" :[ 10,  0.9,  5,  3,  1.4 ]
                ,'1514.T':[  3,  0.8,  5,  3,  0.8 ]
                ,'1515.T':[  4,  0.8,  5,  4,  0.8 ]
                ,'1518.T':[ 23,  0.2,  5, 23,  0.2 ]
                ,'1766.T':[  9,  0.7,  5,  9,  0.7 ]
                ,'1805.T':[  5,  1.1,  5,  5,  1.1 ]
                ,'1808.T':[ 16,  0.5,  5, 16,  0.5 ]
                ,'1813.T':[  8,  0.7,  5,  8,  0.7 ]
                ,'1820.T':[  5,  0.7,  5,  5,  0.7 ]
                ,'1821.T':[ 12,  1.2,  5, 12,  1.2 ]
                ,'1861.T':[  3,  1.0,  5,  3,  1.0 ]
                ,'1866.T':[  5,  1.0,  5,  5,  1.0 ]
                ,'1885.T':[  9,  0.4,  5,  9,  0.4 ]
                ,'1914.T':[  4,  1.4,  5,  4,  1.4 ]
                ,'1954.T':[  3,  0.9,  5,  3,  0.9 ]
                ,'1963.T':[ 12,  1.0,  5, 12,  1.0 ]
                ,'2109.T':[  5,  1.2,  5,  5,  1.2 ]
                ,'2120.T':[ 18,  0.9,  5, 18,  0.9 ]
                ,'2168.T':[  9,  0.5,  5,  9,  0.5 ]
                ,'2286.T':[ 10,  0.6,  5, 10,  0.6 ]
                ,'2378.T':[ 15,  1.4,  5, 15,  1.4 ]
                ,'2462.T':[ 24,  0.5,  5, 24,  0.5 ]
                ,'2695.T':[ 13,  0.7,  5, 13,  0.7 ]
                ,'2752.T':[  7,  1.3,  5,  7,  1.3 ]
                ,'2767.T':[  3,  1.2,  5,  3,  1.2 ]
                ,'2792.T':[  3,  1.1,  5,  3,  1.1 ]
                ,'4368.T':[  3,  1.5,  5,  3,  1.5 ]
                ,'4527.T':[  3,  0.9,  5,  3,  0.9 ]
                ,'5202.T':[ 24,  0.4,  5, 24,  0.4 ]
                ,'5406.T':[ 12,  1.3,  5, 12,  1.3 ]
                ,'5471.T':[  3,  1.1,  5,  3,  1.1 ]
                ,'5707.T':[ 23,  1.2,  5, 23,  1.2 ]
                ,'5711.T':[  8,  0.5,  5,  8,  0.5 ]
                ,'5741.T':[  2,  1.0,  5,  2,  1.0 ]
                ,'5981.T':[  6,  0.7,  5,  6,  0.7 ]
                ,'6205.T':[  8,  0.9,  5,  8,  0.9 ]
                ,'6440.T':[  7,  0.8,  5,  7,  0.8 ]
                ,'6815.T':[  7,  0.7,  5,  7,  0.7 ]
                ,'6866.T':[  4,  1.3,  5,  4,  1.3 ]
                ,'7003.T':[ 10,  1.0,  5, 10,  1.0 ]
                ,'7012.T':[  8,  1.1,  5,  8,  1.1 ]
                ,'7201.T':[  7,  1.4,  5,  7,  1.4 ]
                ,'7513.T':[  4,  0.9,  5,  4,  0.9 ]
                ,'7599.T':[ 17,  1.3,  5, 17,  1.3 ]
                ,'7732.T':[  4,  0.9,  5,  4,  0.9 ]
                ,'8136.T':[ 19,  0.4,  5, 19,  0.4 ]
                ,'8303.T':[ 21,  0.5,  5, 21,  0.5 ]
                ,'8377.T':[  4,  0.6,  5,  4,  0.6 ]
                ,'8473.T':[  8,  0.7,  5,  8,  0.7 ]
                ,'8601.T':[  4,  0.8,  5,  4,  0.8 ]
                ,'8613.T':[  4,  1.5,  5,  4,  1.5 ]
                ,'8698.T':[  8,  0.5,  5,  8,  0.5 ]
                ,'8801.T':[  4,  0.9,  5,  4,  0.9 ]
                ,'8904.T':[  8,  0.3,  5,  8,  0.3 ]
                ,'9101.T':[ 23,  0.3,  5, 23,  0.3 ]
                ,'2501.T':[ 14,  0.4,  5, 14,  0.4 ]
                ,'2729.T':[  4,  1.8,  5,  4,  1.8 ]
                ,'3004.T':[  2,  0.6,  5,  2,  0.6 ]
                ,'3526.T':[ 23,  0.2,  5, 23,  0.2 ]
                ,'4022.T':[  7,  1.2,  5,  7,  1.2 ]
                ,'4298.T':[ 13,  0.4,  5, 13,  0.4 ]
                ,'4641.T':[ 21,  1.4,  5, 21,  1.4 ]
                ,'4971.T':[  3,  1.3,  5,  3,  1.3 ]
                ,'5391.T':[ 23,  0.1,  5, 23,  0.1 ]
                ,'5410.T':[  8,  0.4,  5,  8,  0.4 ]
                ,'5464.T':[  3,  1.7,  5,  3,  1.7 ]
                ,'7236.T':[  3,  0.3,  5,  3,  0.3 ]
                ,'5491.T':[  6,  0.5,  5,  6,  0.5 ]
                ,'5541.T':[ 17,  0.2,  5, 17,  0.2 ]
                ,'5715.T':[ 17,  0.6,  5, 17,  0.6 ]
                ,'5807.T':[  5,  1.4,  5,  5,  1.4 ]
                ,'5998.T':[ 13,  1.3,  5, 13,  1.3 ]
                ,'6104.T':[  4,  0.4,  5,  4,  0.4 ]
                ,'6236.T':[  2,  1.4,  5,  2,  1.4 ]
                ,'6298.T':[  3,  0.4,  5,  3,  0.4 ]
                ,'6315.T':[  6,  1.6,  5,  6,  1.6 ]
                ,'1605.T':[  5,  1.3,  5,  5,  1.3 ]
                ,'1809.T':[  5,  0.9,  5,  5,  0.9 ]
                ,'2428.T':[  4,  1.1,  5,  4,  1.1 ]
                ,'2768.T':[  3,  1.0,  5,  3,  1.0 ]
                ,'3068.T':[  3,  1.0,  5,  3,  1.0 ]
                ,'3116.T':[  8,  0.3,  5,  8,  0.3 ]
                ,'3401.T':[  8,  0.6,  5,  8,  0.6 ]
                ,'4004.T':[  6,  1.2,  5,  6,  1.2 ]
                ,'4043.T':[ 13,  0.5,  5, 13,  0.5 ]
                ,'4062.T':[ 24,  0.6,  5, 24,  0.6 ]
                ,'1356.T':[  4,  1.4,  5,  4,  1.4 ]
                ,'4183.T':[  5,  1.3,  5,  5,  1.3 ]
                ,'4502.T':[ 24,  0.1,  5, 24,  0.1 ]
                ,'4661.T':[ 24,  1.5,  5, 24,  1.5 ]
                ,'4716.T':[ 23,  0.2,  5, 23,  0.2 ]
                ,'5105.T':[ 10,  0.2,  5, 10,  0.2 ]
                ,'5201.T':[ 24,  0.4,  5, 24,  0.4 ]
                ,'5232.T':[  3,  1.0,  5,  3,  1.0 ]
                ,'5233.T':[  3,  1.1,  5,  3,  1.1 ]
                ,'5310.T':[  1,  1.0,  5,  1,  1.0 ]
                ,'5333.T':[ 13,  0.7,  5, 13,  0.7 ]
                ,'5401.T':[  5,  1.7,  5,  5,  1.7 ]
                ,'5411.T':[ 19,  0.7,  5, 19,  0.7 ]
                ,'5480.T':[ 18,  1.9,  5, 18,  1.9 ]
                ,'5563.T':[ 22,  0.9,  5, 22,  0.9 ]
                ,'5706.T':[  5,  0.7,  5,  5,  0.7 ]
                ,'5726.T':[  2,  0.5,  5,  2,  0.5 ]
                ,'5727.T':[  3,  1.0,  5,  3,  1.0 ]
                ,'5803.T':[ 17,  0.2,  5, 17,  0.2 ]
                ,'6103.T':[  6,  0.9,  5,  6,  0.9 ]
                ,'6269.T':[  9,  1.3,  5,  9,  1.3 ]
                ,'6302.T':[  8,  0.3,  5,  8,  0.3 ]
                ,'6305.T':[ 17,  0.5,  5, 17,  0.5 ]
                ,'6310.T':[  6,  0.7,  5,  6,  0.7 ]
                ,'6366.T':[ 18,  1.1,  5, 18,  1.1 ]
                ,'6460.T':[  3,  1.0,  5,  3,  1.0 ]
                ,'6474.T':[  3,  0.5,  5,  3,  0.5 ]
                ,'6501.T':[  3,  1.0,  5,  3,  1.0 ]
                ,'6674.T':[ 15,  0.6,  5, 15,  0.6 ]
                ,'6701.T':[  8,  2.1,  5,  8,  2.1 ]
                ,'6724.T':[ 15,  0.9,  5, 15,  0.9 ]
                ,'6758.T':[  3,  2.1,  5,  3,  2.1 ]
                ,'6803.T':[  3,  0.9,  5,  3,  0.9 ]
                ,'7011.T':[ 10,  0.2,  5, 10,  0.2 ]
                ,'7189.T':[  5,  0.7,  5,  5,  0.7 ]
                ,'7203.T':[  9,  0.7,  5,  9,  0.7 ]
                ,'7211.T':[ 11,  0.6,  5, 11,  0.6 ]
                ,'6135.T':[  3,  1.0,  5,  3,  1.0 ]
                ,'7241.T':[  5,  0.2,  5,  5,  0.2 ]
                ,'7242.T':[  6,  1.1,  5,  6,  1.1 ]
                ,'7261.T':[ 11,  1.1,  5, 11,  1.1 ]
                ,'7550.T':[ 23,  0.2,  5, 23,  0.2 ]
                ,'7581.T':[  4,  0.8,  5,  4,  0.8 ]
                ,'7860.T':[  5,  0.6,  5,  5,  0.6 ]
                ,'7974.T':[  2,  1.4,  5,  2,  1.4 ]
                ,'8031.T':[  3,  1.1,  5,  3,  1.1 ]
                ,'8053.T':[  8,  1.1,  5,  8,  1.1 ]
                ,'8078.T':[  3,  0.6,  5,  3,  0.6 ]
                ,'8267.T':[ 15,  0.8,  5, 15,  0.8 ]
                ,'8316.T':[  3,  1.0,  5,  3,  1.0 ]
                ,'8338.T':[  3,  1.1,  5,  3,  1.1 ]
                ,'8511.T':[  3,  0.7,  5,  3,  0.7 ]
                ,'8570.T':[  3,  1.0,  5,  3,  1.0 ]
                ,'8591.T':[  4,  1.3,  5,  4,  1.3 ]
                ,'8595.T':[  7,  0.8,  5,  7,  0.8 ]
                ,'8604.T':[ 20,  0.4,  5, 20,  0.4 ]
                ,'8086.T':[  2,  1.4,  5,  2,  1.4 ]
                ,'8616.T':[  3,  1.0,  5,  3,  1.0 ]
                ,'8628.T':[  9,  0.4,  5,  9,  0.4 ]
                ,'8703.T':[ 24,  0.3,  5, 24,  0.3 ]
                ,'8830.T':[ 24,  0.3,  5, 24,  0.3 ]
                ,'9001.T':[ 17,  1.0,  5, 17,  1.0 ]
                ,'9005.T':[  4,  1.3,  5,  4,  1.3 ]
                ,'9008.T':[  3,  0.7,  5,  3,  0.7 ]
                ,'9041.T':[  4,  0.6,  5,  4,  0.6 ]
                ,'9062.T':[  3,  0.6,  5,  3,  0.6 ]
                ,'9202.T':[ 14,  0.5,  5, 14,  0.5 ]
                ,'9474.T':[  4,  0.6,  5,  4,  0.6 ]
                ,'9501.T':[ 24,  0.3,  5, 24,  0.3 ]
                ,'9983.T':[ 19,  0.2,  5, 19,  0.2 ]
                ,'5019.T':[  3,  1.9,  5,  3,  1.9 ]
                ,'3101.T':[  4,  1.4,  5,  4,  1.4 ]
                ,'3103.T':[ 10,  0.9,  5, 10,  0.9 ]
                ,'4028.T':[ 16,  0.5,  5, 16,  0.5 ]
                ,'6361.T':[  4,  2.2,  5,  4,  2.2 ]
                ,'6728.T':[  8,  2.0,  5,  8,  2.0 ]
                ,'7004.T':[  7,  1.4,  5,  7,  1.4 ]
                ,'7013.T':[  3,  1.1,  5,  3,  1.1 ]
                ,'7616.T':[  3,  0.7,  5,  3,  0.7 ]
                ,'8233.T':[  3,  0.9,  5,  3,  0.9 ]
                ,"USDJPY":[  5,  0.9,  5,  5,  2.0 ]
                }
    if brute_force:
        bruteforce_open_backtest_breakout_bbsigma1_close_newvalue(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio, long_flg, short_flg)
    else:
        #デフォルトのパラメータ
        long_sma_span = 3
        long_sigma1_ratio = 1.0
        vol_sma_span = 5
        short_sma_span = 3
        short_sigma1_ratio = 1.0
        #symbolごとのparameter
        if symbol in params:
            long_sma_span = params[symbol][0]
            long_sigma1_ratio = params[symbol][1]
            vol_sma_span = params[symbol][2]
            short_sma_span = params[symbol][3]
            short_sigma1_ratio = params[symbol][4]
        backtest_open_breakout_bbsigma1_close_newvalue_asym(symbol
                                                    , ashi
                                                    , start_date
                                                    , end_date
                                                    , long_sma_span
                                                    , long_sigma1_ratio
                                                    , vol_sma_span
                                                    , short_sma_span
                                                    , short_sigma1_ratio
                                                    , initial_cash
                                                    , leverage
                                                    , losscut_ratio
                                                    )
    logger.info("backtest end")

if __name__ == '__main__':
    s = Logger()
    args = get_option()
    if args.symbol is None:
        symbols = Symbol.symbols
    else:
        symbols = args.symbol.split(',')
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
                                                                    , True
                                                                    , True
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



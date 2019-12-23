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
from donkatsu.technical_indicator.average_true_range import AverageTrueRange
from donkatsu.technical_indicator.exponentially_smoothed_movingaverage import ExponentiallySmoothedMovingAverage
from donkatsu.entry_strategy.breakout_atr import BreakoutATR
from donkatsu.exit_strategy.contract_gain_loss import ContractGainLoss

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

def backtest_open_breakout_atr_close_atr(symbol
                                                        , ashi
                                                        , start_date
                                                        , end_date
                                                        , long_atr_span
                                                        , long_atr_ratio
                                                        , vol_ema_span
                                                        , short_atr_span
                                                        , short_atr_ratio
                                                        , close_atr_span
                                                        , atr_profit_ratio
                                                        , atr_loss_ratio
                                                        , specified_profit_ratio
                                                        , specified_loss_ratio
                                                        , initial_cash
                                                        , leverage
                                                        , losscut_ratio
                                                        ):
    contract_gain_method = 2
    asset = Asset(symbol, initial_cash, leverage, losscut_ratio)
    ohlcv = Ohlcv(symbol, ashi, start_date, end_date)
    long_atr = AverageTrueRange(ohlcv, long_atr_span, long_atr_ratio)
    short_atr = AverageTrueRange(ohlcv, short_atr_span, long_atr_ratio)
    vol_ema = ExponentiallySmoothedMovingAverage(ohlcv, vol_ema_span, vol_ema_span)
    open_title = f"BreakOutATR:[{long_atr_span:.0f},{long_atr_ratio:.2f}][{short_atr_span:.0f},{short_atr_ratio:.2f}]"
    close_title = f"Contract:[{contract_gain_method}][{atr_profit_ratio:.4f},{atr_loss_ratio:.4f}][{specified_profit_ratio:.4f},{specified_loss_ratio:.4f}]"
    open_strategy = BreakoutATR(open_title, ohlcv, long_atr, short_atr, vol_ema)
    close_atr = AverageTrueRange(ohlcv, close_atr_span)
    close_strategy = ContractGainLoss(close_title, ohlcv, contract_gain_method, atr_profit_ratio, atr_loss_ratio, close_atr, specified_profit_ratio, specified_loss_ratio)
    #exit_strategy = ContractGainLoss(close_title, ohlcv, close_atr, atr_profit_ratio, atr_loss_ratio, specified_profit_ratio, specified_loss_ratio)
    Market().simulator_run(ohlcv, open_strategy, close_strategy, asset) 

def bruteforce_backtest(symbol):
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
                 "^N225":[ 3, 0.5, 5, 3, 0.5 , 3, 0.5, 0.1, 0.03]
                #"1570.T":[ ]
                #,"1568.T":[ ]
                #,"1357.T":[ ]
                #,"1356.T":[ ]
                #,"5801.T":[ ]
                #,"5631.T":[ ]
                #,"6141.T":[ ]
                #,"6753.T":[ ]
                #,"9104.T":[ ]
                #,"9107.T":[ ]
                }
    if brute_force:
        #bruteforce_backtest(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio, long_flg, short_flg)
        pass
    else:
        #デフォルトのパラメータ
        long_atr_span = 3
        long_atr_ratio = 0.5
        vol_sma_span = 5
        short_atr_span = 3
        short_atr_ratio = 0.5
        close_atr_span = 3
        atr_profit_ratio = 0.6 #ATRの乗数
        atr_loss_ratio = 0.2 #ATRの乗数
        specified_profit_ratio = 0.1 #利益率
        specified_loss_ratio = 0.03 #利益率
        losscut_ratio = 0.03
        #symbolごとのparameter
        if symbol in params:
            long_atr_span = params[symbol][0]
            long_atr_ratio = params[symbol][1]
            vol_sma_span = params[symbol][2]
            short_atr_span = params[symbol][3]
            short_atr_ratio = params[symbol][4]
            close_atr_span = params[symbol][5]
            atr_profit_ratio = params[symbol][6]
            atr_loss_ratio = params[symbol][7]
        backtest_open_breakout_atr_close_atr(symbol
                                            , ashi
                                            , start_date
                                            , end_date
                                            , long_atr_span
                                            , long_atr_ratio
                                            , vol_sma_span
                                            , short_atr_span
                                            , short_atr_ratio
                                            , close_atr_span
                                            , atr_profit_ratio
                                            , atr_loss_ratio
                                            , specified_profit_ratio
                                            , specified_loss_ratio
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
        #backtest(symbol, ashi, start_date, end_date, True, True, True)
        #backtest(symbol, ashi, start_date, end_date, False, False, False)
        backtest(s, ashi, start_date, end_date, brute_force, True, True)


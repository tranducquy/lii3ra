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
from donkatsu.technical_indicator.bollingerband import Bollingerband
from donkatsu.entry_strategy.classic_bollingerbands import ClassicBollingerbands
from donkatsu.exit_strategy.newvalue import Newvalue

# from donkatsu.symbol.test import Symbol
# from donkatsu.symbol.bollingerband_newvalue import Symbol
# from donkatsu.symbol.n225 import Symbol
from donkatsu.symbol.n225_topix import Symbol

s = Logger()
logger = s.myLogger()

# parameters
params = {
}


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('--symbol', type=str, help='Absolute/relative path to input file')
    argparser.add_argument('--start_date', type=str, help='Date of backtest start')
    argparser.add_argument('--end_date', type=str, help='Date of backtest end')
    argparser.add_argument('--brute_force', action='store_true', help='breaking the code!')
    argparser.add_argument('--strategy', type=str, help='Choose Strategy!')
    argparser.add_argument('--ashi', type=str, help='ASHI!')
    return argparser.parse_args()

def backtest_run(symbol
                 , ashi
                 , start_date
                 , end_date
                 , bb_period
                 , sigma1_ratio
                 , lookback
                 , initial_cash
                 , leverage
                 , losscut_ratio
                 ):
    try:
        asset = Asset(symbol, initial_cash, leverage, losscut_ratio)
        ohlcv = Ohlcv(symbol, ashi, start_date, end_date)
        bb = Bollingerband(ohlcv, bb_period, sigma1_ratio)
        open_title = f"ClassicBollingerBands[{bb_period:.0f},{sigma1_ratio:.2f},{lookback:.0f}]"
        close_title = f"NewValue"
        open_strategy = ClassicBollingerbands(open_title, ohlcv, bb, sigma1_ratio, lookback)
        close_strategy = Newvalue(close_title, ohlcv)
        Market().simulator_run(ohlcv, open_strategy, close_strategy, asset)
    except Exception as err:
        print(err)


def bruteforce_backtest(symbol
                        , ashi
                        , start_date
                        , end_date
                        , initial_cash
                        , leverage
                        , losscut_ratio
                        , long_flg
                        , short_flg
                        ):
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
        # bruteforce_backtest(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio, True, False)
        # bruteforce_backtest(symbol, ashi, start_date, end_date, initial_cash, leverage, losscut_ratio, False, True)
        pass
    else:
        # デフォルトのパラメータ
        bb_period     =   20
        sigma1_ratio  =    2
        lookback      =   20
        # symbolごとのparameter
        if symbol in params:
            bb_period = params[symbol][0]
            sigma1_ratio = params[symbol][1]
            lookback = params[symbol][2]
        backtest_run(symbol
                     , ashi
                     , start_date
                     , end_date
                     , bb_period
                     , sigma1_ratio
                     , lookback
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
        start_date = (datetime.today() - relativedelta(months=3)).strftime('%Y-%m-%d')  # 今日の3か月前
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

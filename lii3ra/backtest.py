#! /usr/bin/env python
# -*- coding: utf-8 -*-

from lii3ra.mylogger import Logger
from lii3ra.market import Market
from lii3ra.asset import Asset
from lii3ra.ohlcv import Ohlcv
from lii3ra.entry_strategy.breakout_sigma1 import BreakoutSigma1Factory
from lii3ra.entry_strategy.breakout_with_a_twist import BreakoutWithTwistFactory
from lii3ra.exit_strategy.newvalue import NewvalueFactory
from lii3ra.exit_strategy.timed import TimedFactory

# from lii3ra.symbol.test import Symbol
# from lii3ra.symbol.bollingerband_newvalue import Symbol
# from lii3ra.symbol.topix17etf_nomura import Symbol
# from lii3ra.symbol.n225 import Symbol
# from lii3ra.symbol.n225_topix import Symbol

s = Logger()
logger = s.myLogger()


def strategy_comination(symbol, ashi, start_date, end_date):
    logger.info("backtest start")
    logger.info(f"parameter symbol={symbol}, ashi={ashi}, start_date={start_date}, end_date={end_date}")
    initial_cash = 1000000
    leverage = 3.0
    losscut_ratio = 0.03
    try:
        entry_strategies = []
        exit_strategies = []
        ohlcv = Ohlcv(symbol, ashi, start_date, end_date)
        # ENTRY
        # BREAKOUT SIGMA1
        entry_strategies.append(BreakoutSigma1Factory().create_strategy(ohlcv))
        # BREAKOUT WITH A TWIST
        entry_strategies.append(BreakoutWithTwistFactory().create_strategy(ohlcv))
        # EXIT
        # NEWVALUE
        exit_strategies.append(NewvalueFactory().create_strategy(ohlcv))
        # TIMED
        exit_strategies.append(TimedFactory().create_strategy(ohlcv))
        for entry_strategy in entry_strategies:
            for exit_strategy in exit_strategies:
                asset = Asset(symbol, initial_cash, leverage, losscut_ratio)
                Market().simulator_run(ohlcv, entry_strategy, exit_strategy, asset)
    except Exception as err:
        print(err)
    logger.info("backtest end")


def optimization_entry(symbol, ashi, start_date, end_date, rough=True):
    logger.info("backtest bruteforce entry start")
    logger.info(f"parameter symbol={symbol}, ashi={ashi}, start_date={start_date}, end_date={end_date}")
    initial_cash = 1000000
    leverage = 3.0
    losscut_ratio = 0.03
    try:
        entry_strategies = []
        ohlcv = Ohlcv(symbol, ashi, start_date, end_date)
        # ENTRY
        # BREAKOUT SIGMA1
        entry_strategies.extend(BreakoutSigma1Factory().optimization(ohlcv, rough))
        # BREAKOUT WITH A TWIST
        entry_strategies.extend(BreakoutWithTwistFactory().optimization(ohlcv, rough))
        # EXIT
        # NEWVALUE
        exit_strategy = NewvalueFactory().create_strategy(ohlcv)
        # TIMED
        # exit_strategy = TimedFactory().create_strategy(ohlcv)
        for entry_strategy in entry_strategies:
            asset = Asset(symbol, initial_cash, leverage, losscut_ratio)
            Market().simulator_run(ohlcv, entry_strategy, exit_strategy, asset)
    except Exception as err:
        print(err)
    logger.info("backtest bruteforce entry end")


def optimization_exit(symbol, ashi, start_date, end_date, rough=True):
    logger.info("backtest bruteforce exit start")
    logger.info(f"parameter symbol={symbol}, ashi={ashi}, start_date={start_date}, end_date={end_date}")
    initial_cash = 1000000
    leverage = 3.0
    losscut_ratio = 0.03
    try:
        exit_strategies = []
        ohlcv = Ohlcv(symbol, ashi, start_date, end_date)
        # ENTRY
        # BREAKOUT SIGMA1
        # entry_strategy = BreakoutSigma1Factory().create_strategy(ohlcv)
        # BREAKOUT WITH A TWIST
        entry_strategy = BreakoutWithTwistFactory().create_strategy(ohlcv)
        # EXIT
        # NEWVALUE
        exit_strategies.extend(NewvalueFactory().optimization(ohlcv, rough))
        # TIMED
        exit_strategies.extend(TimedFactory().optimization(ohlcv, rough))
        for exit_strategy in exit_strategies:
            asset = Asset(symbol, initial_cash, leverage, losscut_ratio)
            Market().simulator_run(ohlcv, entry_strategy, exit_strategy, asset)
    except Exception as err:
        print(err)
    logger.info("backtest bruteforce exit end")


if __name__ == '__main__':
    symbol = "^N225"
    ashi = "1d"
    start_date = "2010-01-01"
    end_date = "2019-12-31"
    rough = True
    strategy_comination(symbol, ashi, start_date, end_date)
    # optimization_entry(symbol, ashi, start_date, end_date, rough)
    # optimization_exit(symbol, ashi, start_date, end_date, rough)



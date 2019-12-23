#! /usr/bin/env python
# -*- coding: utf-8 -*-

from lii3ra.mylogger import Logger
from lii3ra.market import Market
from lii3ra.asset import Asset
from lii3ra.ohlcv import Ohlcv
from lii3ra.entry_strategy.breakout_sigma1 import BreakoutSigma1Factory
from lii3ra.exit_strategy.newvalue import NewvalueFactory

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
        asset = Asset(symbol, initial_cash, leverage, losscut_ratio)
        ohlcv = Ohlcv(symbol, ashi, start_date, end_date)
        entry_strategy = BreakoutSigma1Factory().create_strategy(ohlcv)
        exit_strategy = NewvalueFactory.create_strategy(ohlcv)
        Market().simulator_run(ohlcv, entry_strategy, exit_strategy, asset)
    except Exception as err:
        print(err)
    logger.info("backtest end")


def optimization_rough(symbol, ashi, start_date, end_date):
    logger.info("backtest rough start")
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
        entry_strategies.extend(BreakoutSigma1Factory().optimization_rough(ohlcv))
        # EXIT
        # NEWVALUE
        exit_strategies.extend(NewvalueFactory().optimization_rough(ohlcv))
        for entry_strategy in entry_strategies:
            for exit_strategy in exit_strategies:
                asset = Asset(symbol, initial_cash, leverage, losscut_ratio)
                Market().simulator_run(ohlcv, entry_strategy, exit_strategy, asset)
    except Exception as err:
        print(err)
    logger.info("backtest rough end")


def optimization(symbol, ashi, start_date, end_date):
    logger.info("backtest bruteforce start")
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
        entry_strategies.extend(BreakoutSigma1Factory().optimization(ohlcv))
        # EXIT
        # NEWVALUE
        exit_strategies.extend(NewvalueFactory().optimization(ohlcv))
        for entry_strategy in entry_strategies:
            for exit_strategy in exit_strategies:
                asset = Asset(symbol, initial_cash, leverage, losscut_ratio)
                Market().simulator_run(ohlcv, entry_strategy, exit_strategy, asset)
    except Exception as err:
        print(err)
    logger.info("backtest bruteforce end")


if __name__ == '__main__':
    symbol = "^N225"
    ashi = "1d"
    start_date = "2010-01-01"
    end_date = "2019-12-31"
    # strategy_comination(symbol, ashi, start_date, end_date)
    optimization_rough(symbol, ashi, start_date, end_date)
    # optimization(symbol, ashi, start_date, end_date)


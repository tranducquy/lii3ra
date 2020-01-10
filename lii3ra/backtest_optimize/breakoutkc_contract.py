#! /usr/bin/env python
# -*- coding: utf-8 -*-


import threading
import numpy as np
from lii3ra.mylogger import Logger
from lii3ra.market import Market
from lii3ra.asset import Asset
from lii3ra.ohlcv import Ohlcv
# ENTRY
from lii3ra.entry_strategy.breakout_kc import BreakoutKCFactory
# EXIT
from lii3ra.exit_strategy.contract_gain_loss import ContractGainLossFactory


s = Logger()
logger = s.myLogger()


def combination_strategy(symbol, ashi, start_date, end_date, asset_values):
    logger.info("backtest start")
    logger.info(f"parameter symbol={symbol}, ashi={ashi}, start_date={start_date}, end_date={end_date}")
    try:
        entry_strategies = []
        exit_strategies = []
        ohlcv = Ohlcv(symbol, ashi, start_date, end_date)
        # ENTRY
        entry_strategies.append(BreakoutKCFactory().create_strategy(ohlcv))
        # EXIT
        exit_strategies.append(ContractGainLossFactory().create_strategy(ohlcv))  # CONTRACT GAIN AND LOSS
        thread_pool = list()
        for entry_strategy in entry_strategies:
            for exit_strategy in exit_strategies:
                asset = Asset(symbol
                              , asset_values["initial_cash"]
                              , asset_values["leverage"]
                              , asset_values["losscut_ratio"])
                thread_pool.append(threading.Thread(target=Market().simulator_run, args=(ohlcv
                                                                                         , entry_strategy
                                                                                         , exit_strategy
                                                                                         , asset
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
    except Exception as err:
        print(err)
    logger.info("backtest end")


def optimization_entry(symbol, ashi, start_date, end_date, asset_values, rough=True):
    logger.info("backtest bruteforce entry start")
    logger.info(f"parameter symbol={symbol}, ashi={ashi}, start_date={start_date}, end_date={end_date}")
    try:
        entry_strategies = []
        ohlcv = Ohlcv(symbol, ashi, start_date, end_date)
        # ENTRY
        entry_strategies.extend(BreakoutKCFactory().optimization(ohlcv, rough))
        # EXIT
        exit_strategy = ContractGainLossFactory().create_strategy(ohlcv)                   # CONTRACT GAIN AND LOSS
        thread_pool = list()
        for entry_strategy in entry_strategies:
            asset = Asset(symbol
                          , asset_values["initial_cash"]
                          , asset_values["leverage"]
                          , asset_values["losscut_ratio"])
            thread_pool.append(threading.Thread(target=Market().simulator_run, args=(ohlcv
                                                                                     , entry_strategy
                                                                                     , exit_strategy
                                                                                     , asset
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
    except Exception as err:
        print(err)
    logger.info("backtest bruteforce entry end")


def optimization_exit(symbol, ashi, start_date, end_date, asset_values, rough=True):
    logger.info("backtest bruteforce exit start")
    logger.info(f"parameter symbol={symbol}, ashi={ashi}, start_date={start_date}, end_date={end_date}")
    try:
        exit_strategies = []
        ohlcv = Ohlcv(symbol, ashi, start_date, end_date)
        # ENTRY
        entry_strategy = BreakoutKCFactory().create_strategy(ohlcv)
        # EXIT
        exit_strategies.extend(ContractGainLossFactory().optimization(ohlcv, rough))      # CONTRACT GAIN AND LOSS
        thread_pool = list()
        for exit_strategy in exit_strategies:
            asset = Asset(symbol
                          , asset_values["initial_cash"]
                          , asset_values["leverage"]
                          , asset_values["losscut_ratio"])
            thread_pool.append(threading.Thread(target=Market().simulator_run, args=(ohlcv
                                                                                     , entry_strategy
                                                                                     , exit_strategy
                                                                                     , asset
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

    except Exception as err:
        print(err)
    logger.info("backtest bruteforce exit end")


if __name__ == '__main__':
    from lii3ra.symbol.volume_10b import Symbol
    symbol_list = Symbol.symbols

    # ashi
    ashi = "1d"
    # ashi = "15m"

    # range
    start_date = "2019-01-01"
    end_date = "2019-12-31"

    # その他
    asset_values = {"initial_cash": 1000000, "leverage": 3.0, "losscut_ratio": 0.05}
    rough = True
    # rough = False

    for symbol in symbol_list:
        combination_strategy(symbol, ashi, start_date, end_date, asset_values)
        # optimization_entry(symbol, ashi, start_date, end_date, asset_values, rough)
        # optimization_exit(symbol, ashi, start_date, end_date, asset_values, rough)


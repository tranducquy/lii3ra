#! /usr/bin/env python
# -*- coding: utf-8 -*-

from lii3ra.symbol.topix17etf.topix17etf_nomura import Symbol

import threading
import numpy as np
from lii3ra.mylogger import Logger
from lii3ra.market import Market
from lii3ra.asset import Asset
from lii3ra.ohlcv import Ohlcv
# ENTRY
from lii3ra.entry_strategy.breakout_sigma1 import BreakoutSigma1Factory
from lii3ra.entry_strategy.go_with_the_flow import GoWithTheFlowFactory
from lii3ra.entry_strategy.breakout_with_a_twist import BreakoutWithTwistFactory
from lii3ra.entry_strategy.everyone_loves_friday import EveryoneLovesFridayFactory  # 2
from lii3ra.entry_strategy.books_can_be_great import BooksCanBeGreatFactory  # 3
from lii3ra.entry_strategy.atr_based_breakout import ATRBasedBreakoutFactory  # 5
from lii3ra.entry_strategy.percent_ranker import PercentRankerFactory  # 6
from lii3ra.entry_strategy.rsi_trigger import RSITriggerFactory  # 12
from lii3ra.entry_strategy.ma_with_a_twist import MAWithTwistFactory  # 13
from lii3ra.entry_strategy.split_week import SplitWeekFactory  # 14
from lii3ra.entry_strategy.introducing_serial_correlation import IntroducingSerialCorrelationFactory  # 16
from lii3ra.entry_strategy.back_in_style import BackInStyleFactory  # 17
from lii3ra.entry_strategy.where_you_at import WhereYouAtFactory  # 18
from lii3ra.entry_strategy.exponentially_better import ExponentiallyBetterFactory  # 19
from lii3ra.entry_strategy.asymmetric_triple import AsymmetricTripleFactory  # 21
from lii3ra.entry_strategy.asymmetric_again import AsymmetricAgainFactory  # 22
from lii3ra.entry_strategy.stochastic_cross import StochasticCrossFactory  # 23
from lii3ra.entry_strategy.show_me_the_money import ShowMeTheMoneyFactory  # 24
from lii3ra.entry_strategy.classic_bollingerbands import ClassicBollingerbandsFactory  # 25
from lii3ra.entry_strategy.classic_keltner_channel import ClassicKeltnerChannelFactory  # 26
from lii3ra.entry_strategy.three_amigos import ThreeAmigosFactory  # 27
from lii3ra.entry_strategy.two_amigos import TwoAmigosFactory  # 28
from lii3ra.entry_strategy.pitter_patter_pattern import PitterPatterPatternFactory  # 29
from lii3ra.entry_strategy.pitter_patter_pattern2 import PitterPatterPattern2Factory  # 30
from lii3ra.entry_strategy.closing_pattern_only import ClosingPatternOnlyFactory  # 31
from lii3ra.entry_strategy.quick_pullback_pattern import QuickPullbackPatternFactory  # 32
from lii3ra.entry_strategy.closing_pattern_only2 import ClosingPatternOnly2Factory  # 33
from lii3ra.entry_strategy.breakdown_dead_ahead import BreakdownDeadAheadFactory  # 34
from lii3ra.entry_strategy.commodity_channel_index import EntryCommodityChannelIndexFactory  # 35
from lii3ra.entry_strategy.big_tail_bars import BigTailBarsFactory  # 36
from lii3ra.entry_strategy.newhigh_with_consecutive_highs import NewHighWithConsecutiveHighsFactory  # 37
from lii3ra.entry_strategy.start_with_an_awesome_oscillator import StartWithAwesomeOscillatorFactory  # 38
from lii3ra.entry_strategy.second_verse_same_as_the_first import SecondVerseSameAsTheFirstFactory  # 39
from lii3ra.entry_strategy.its_about_time import ItsAboutTimeFactory  # 40
from lii3ra.entry_strategy.filtered_entry import FilteredEntryFactory  # 41
from lii3ra.entry_strategy.intraday_breakout import IntradayBreakoutFactory  # 7
from lii3ra.entry_strategy.intraday_breakout_with_expanding_range import IntradayBreakoutWithExpandingRangeFactory  # 8
from lii3ra.entry_strategy.day_of_week import DayOfWeekFactory  # 9
from lii3ra.entry_strategy.enhanced_economic_calender import EnhancedEconomicCalenderFactory
from lii3ra.entry_strategy.range_breakout import RangeBreakoutFactory  # 20
from lii3ra.entry_strategy.the_ultimate import TheUltimateFactory  # Bonus 1
from lii3ra.entry_strategy.economic_calender import EconomicCalenderFactory  # Bonus 2
# EXIT
from lii3ra.exit_strategy.newvalue import NewvalueFactory
from lii3ra.exit_strategy.timed import TimedFactory
from lii3ra.exit_strategy.timed_by_time import TimedByTimeFactory
from lii3ra.exit_strategy.contract_gain_loss import ContractGainLossFactory
from lii3ra.exit_strategy.percentile import PercentileFactory
from lii3ra.exit_strategy.getting_is_good import GettingIsGoodFactory
from lii3ra.exit_strategy.end_of_bar import EndOfBarFactory
from lii3ra.exit_strategy.dont_give_it_all_back import DontGiveItAllBackFactory
from lii3ra.exit_strategy.profit_protector import ProfitProtectorFactory
from lii3ra.exit_strategy.exit_where_you_like import ExitWhereYouLikeFactory
from lii3ra.exit_strategy.tiered import TieredFactory


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
        entry_strategies.append(BreakoutWithTwistFactory().create_strategy(ohlcv))  # BREAKOUT WITH A TWIST
        # EXIT
        exit_strategies.append(NewvalueFactory().create_strategy(ohlcv))  # NEWVALUE
        exit_strategies.append(TimedFactory().create_strategy(ohlcv))  # TIMED
        exit_strategies.append(ContractGainLossFactory().create_strategy(ohlcv))  # CONTRACT GAIN AND LOSS
        exit_strategies.append(PercentileFactory().create_strategy(ohlcv))  # PERCENTILE
        exit_strategies.append(GettingIsGoodFactory().create_strategy(ohlcv))  # GETTING IS GOOD
        exit_strategies.append(EndOfBarFactory().create_strategy(ohlcv))  # END OF BAR
        exit_strategies.append(DontGiveItAllBackFactory().create_strategy(ohlcv))  # DON'T GIVE IT ALL BACK
        exit_strategies.append(ProfitProtectorFactory().create_strategy(ohlcv))  # PROFIT PROTECTOR
        exit_strategies.append(ExitWhereYouLikeFactory().create_strategy(ohlcv))  # EXIT WHERE YOU LIKE
        exit_strategies.append(TieredFactory().create_strategy(ohlcv))  # TIERED
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
        entry_strategies.extend(BreakoutWithTwistFactory().optimization(ohlcv, rough))     # BREAKOUT WITH A TWIST
        # EXIT
        # exit_strategy = NewvalueFactory().create_strategy(ohlcv)  # NEWVALUE
        exit_strategy = TimedFactory().create_strategy(ohlcv)                            # TIMED
        # exit_strategy = ContractGainLossFactory().create_strategy(ohlcv)                   # CONTRACT GAIN AND LOSS
        # exit_strategy = PercentileFactory().create_strategy(ohlcv)                   # PERCENTILE
        # exit_strategy = GettingIsGoodFactory().create_strategy(ohlcv)                   # GETTING IS GOOD
        # exit_strategy = EndOfBarFactory().create_strategy(ohlcv)                   # END OF BAR
        # exit_strategy = DontGiveItAllBackFactory().create_strategy(ohlcv)                   # DON'T GIVE IT ALL BACK
        # exit_strategy = ProfitProtectorFactory().create_strategy(ohlcv)                   # PROFIT PROTECTOR
        # exit_strategy = ExitWhereYouLikeFactory().create_strategy(ohlcv)                   # EXIT WHERE YOU LIKE
        # exit_strategy = TieredFactory().create_strategy(ohlcv)                               # TIERED
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
        entry_strategy = BreakoutWithTwistFactory().create_strategy(ohlcv)            # BREAKOUT WITH A TWIST
        # EXIT
        exit_strategies.extend(NewvalueFactory().optimization(ohlcv, rough))  # NEWVALUE
        # exit_strategies.extend(TimedFactory().optimization(ohlcv, rough))                 # TIMED
        # exit_strategies.extend(ContractGainLossFactory().optimization(ohlcv, rough))      # CONTRACT GAIN AND LOSS
        # exit_strategies.extend(PercentileFactory().optimization(ohlcv, rough))      # PERCENTILE
        # exit_strategies.extend(GettingIsGoodFactory().optimization(ohlcv, rough))      # GETTING IS GOOD
        # exit_strategies.extend(EndOfBarFactory().optimization(ohlcv, rough))      # END OF BAR
        # exit_strategies.extend(DontGiveItAllBackFactory().optimization(ohlcv, rough))      # DON'T GIVE IT ALL BACK
        # exit_strategies.extend(ProfitProtectorFactory().optimization(ohlcv, rough))      # PROFIT PROTECTOR
        # exit_strategies.extend(ExitWhereYouLikeFactory().optimization(ohlcv, rough))      # EXIT WHERE YOU LIKE
        # exit_strategies.extend(TieredFactory().optimization(ohlcv, rough))                  # TIERED
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
    start_date = "2004-01-01"
    end_date = "2019-12-31"

    # その他
    asset_values = {"initial_cash": 1000000, "leverage": 3.0, "losscut_ratio": 0.05}
    rough = True
    # rough = False

    for symbol in symbol_list:
        # combination_strategy(symbol, ashi, start_date, end_date, asset_values)
        optimization_entry(symbol, ashi, start_date, end_date, asset_values, rough)
        # optimization_exit(symbol, ashi, start_date, end_date, asset_values, rough)


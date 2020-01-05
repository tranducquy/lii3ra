#! /usr/bin/env python
# -*- coding: utf-8 -*-

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
from lii3ra.entry_strategy.breakout_kc import BreakoutKCFactory
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
        # 分足
        # entry_strategies.append(EconomicCalenderFactory().create_strategy(ohlcv))          # ECONOMIC CALENDER
        # entry_strategies.append(EnhancedEconomicCalenderFactory().create_strategy(ohlcv))  # ENHANCED ECONOMIC CALENDER
        # entry_strategies.append(RangeBreakoutFactory().create_strategy(ohlcv))             # RANGE BREAKOUT
        # entry_strategies.append(IntradayBreakoutFactory().create_strategy(ohlcv))          # INTRADAY BREAKOUT
        # entry_strategies.append(IntradayBreakoutWithExpandingRangeFactory().create_strategy(ohlcv))  # INTRADAY BREAKOUT2
        # entry_strategies.append(ItsAboutTimeFactory().create_strategy(ohlcv))              # IT'S ABOUT TIME
        # entry_strategies.append(WhereYouAtFactory().create_strategy(ohlcv))                # WHERE YOU AT
        # 日足
        # entry_strategies.append(EveryoneLovesFridayFactory().create_strategy(ohlcv))  # EVERYONE LOVES FRIDAY
        # entry_strategies.append(SplitWeekFactory().create_strategy(ohlcv))  # SPLIT WEEK
        # entry_strategies.append(DayOfWeekFactory().create_strategy(ohlcv))  # DAY OF WEEK
        # any
        entry_strategies.append(ATRBasedBreakoutFactory().create_strategy(ohlcv))   # ATR BASED BREAKOUT
        entry_strategies.append(AsymmetricAgainFactory().create_strategy(ohlcv))    # ASYMMETRIC AGAIN
        entry_strategies.append(AsymmetricTripleFactory().create_strategy(ohlcv))   # ASYMMETRIC TRIPLE
        entry_strategies.append(BreakoutWithTwistFactory().create_strategy(ohlcv))  # BREAKOUT WITH A TWIST
        entry_strategies.append(BreakoutSigma1Factory().create_strategy(ohlcv))     # BREAKOUT SIGMA1
        entry_strategies.append(BreakoutKCFactory().create_strategy(ohlcv))         # BREAKOUT KC
        entry_strategies.append(RSITriggerFactory().create_strategy(ohlcv))         # RSI TRIGGER
        entry_strategies.append(StochasticCrossFactory().create_strategy(ohlcv))    # STOCHASTIC CROSS
        entry_strategies.append(ThreeAmigosFactory().create_strategy(ohlcv))        # THREE AMIGOS
        entry_strategies.append(TwoAmigosFactory().create_strategy(ohlcv))          # TWO AMIGOS
        entry_strategies.append(TheUltimateFactory().create_strategy(ohlcv))        # THE ULTIMATE
        entry_strategies.append(PercentRankerFactory().create_strategy(ohlcv))      # PERCENT RANKER
        entry_strategies.append(StartWithAwesomeOscillatorFactory().create_strategy(ohlcv))  # START AWESOME
        entry_strategies.append(QuickPullbackPatternFactory().create_strategy(ohlcv))        # QUICK PULLBACK PATTERN

        # entry_strategies.append(ShowMeTheMoneyFactory().create_strategy(ohlcv))  # SHOW ME THE MONEY
        # entry_strategies.append(NewHighWithConsecutiveHighsFactory().create_strategy(ohlcv))  # NEW HIGH
        # entry_strategies.append(BackInStyleFactory().create_strategy(ohlcv))  # BACK IN STYLE
        # entry_strategies.append(BigTailBarsFactory().create_strategy(ohlcv))  # BIG TAIL BARS
        # entry_strategies.append(BooksCanBeGreatFactory().create_strategy(ohlcv))  # BOOKS CAN BE GREAT
        # entry_strategies.append(BreakdownDeadAheadFactory().create_strategy(ohlcv))  # BREAKDOWN DEAD A HEAD
        # entry_strategies.append(ClassicBollingerbandsFactory().create_strategy(ohlcv))  # CLASSIC BOLLINGERBANDS
        # entry_strategies.append(ClassicKeltnerChannelFactory().create_strategy(ohlcv))  # CLASSIC KC
        # entry_strategies.append(ClosingPatternOnlyFactory().create_strategy(ohlcv))  # CLOSING PATTERN ONLY
        # entry_strategies.append(ClosingPatternOnly2Factory().create_strategy(ohlcv))  # CLOSING PATTERN ONLY2
        # entry_strategies.append(EntryCommodityChannelIndexFactory().create_strategy(ohlcv))  # ENTRY CCI
        # entry_strategies.append(GoWithTheFlowFactory().create_strategy(ohlcv))  # GO WITH THE FLOW
        # entry_strategies.append(MAWithTwistFactory().create_strategy(ohlcv))  # MA WITH A TWIST
        # entry_strategies.append(IntroducingSerialCorrelationFactory().create_strategy(ohlcv))  # INTRO SERIAL
        # entry_strategies.append(ExponentiallyBetterFactory().create_strategy(ohlcv))  # EXPONENTIALLY BETTER
        # entry_strategies.append(PitterPatterPatternFactory().create_strategy(ohlcv))  # PITTER PATTER PATTERN
        # entry_strategies.append(PitterPatterPattern2Factory().create_strategy(ohlcv))  # PITTER PATTER PATTERN2
        # entry_strategies.append(SecondVerseSameAsTheFirstFactory().create_strategy(ohlcv))  # SECOND VERSE
        # entry_strategies.append(FilteredEntryFactory().create_strategy(ohlcv))  # FILTERED ENTRY
        # EXIT
        # 分足
        # exit_strategies.append(TimedByTimeFactory().create_strategy(ohlcv))             # TIMED BY TIME
        # 日足
        # any
        exit_strategies.append(NewvalueFactory().create_strategy(ohlcv))           # NEWVALUE
        exit_strategies.append(PercentileFactory().create_strategy(ohlcv))         # PERCENTILE
        exit_strategies.append(TimedFactory().create_strategy(ohlcv))              # TIMED
        exit_strategies.append(EndOfBarFactory().create_strategy(ohlcv))           # END OF BAR
        exit_strategies.append(GettingIsGoodFactory().create_strategy(ohlcv))      # GETTING IS GOOD
        exit_strategies.append(DontGiveItAllBackFactory().create_strategy(ohlcv))  # DON'T GIVE IT ALL BACK
        exit_strategies.append(ContractGainLossFactory().create_strategy(ohlcv))   # CONTRACT GAIN AND LOSS
        exit_strategies.append(ProfitProtectorFactory().create_strategy(ohlcv))    # PROFIT PROTECTOR
        exit_strategies.append(ExitWhereYouLikeFactory().create_strategy(ohlcv))   # EXIT WHERE YOU LIKE
        exit_strategies.append(TieredFactory().create_strategy(ohlcv))             # TIERED
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
        # 分足
        # entry_strategies.extend(EconomicCalenderFactory().optimization(ohlcv, rough))   # ECONOMIC CALENDER
        # entry_strategies.extend(EnhancedEconomicCalenderFactory().optimization(ohlcv, rough))   # ENHANCED ECONOMIC CALENDER
        # entry_strategies.extend(RangeBreakoutFactory().optimization(ohlcv, rough))   # RANGE BREAKOUT
        # entry_strategies.extend(IntradayBreakoutFactory().optimization(ohlcv, rough))   # INTRADAY BREAKOUT
        # entry_strategies.extend(IntradayBreakoutWithExpandingRangeFactory().optimization(ohlcv, rough))   # INTRADAY BREAKOUT2
        # entry_strategies.extend(ItsAboutTimeFactory().optimization(ohlcv, rough))   # IT'S ABOUT TIME
        # entry_strategies.extend(WhereYouAtFactory().optimization(ohlcv, rough))               # WHERE YOU AT
        # 日足
        # entry_strategies.extend(EveryoneLovesFridayFactory().optimization(ohlcv, rough))       # EVERYONE LOVES FRIDAY
        # entry_strategies.extend(SplitWeekFactory().optimization(ohlcv, rough))       # SPLIT WEEK
        # entry_strategies.extend(DayOfWeekFactory().optimization(ohlcv, rough))   # DAY OF WEEK
        # any
        entry_strategies.extend(BreakoutWithTwistFactory().optimization(ohlcv, rough))    # BREAKOUT WITH A TWIST
        entry_strategies.extend(ATRBasedBreakoutFactory().optimization(ohlcv, rough))     # ATR BASED BREAKOUT
        entry_strategies.extend(AsymmetricTripleFactory().optimization(ohlcv, rough))     # ASTMETRIC TRIPLE
        entry_strategies.extend(AsymmetricAgainFactory().optimization(ohlcv, rough))      # ASTMETRIC AGAIN
        entry_strategies.extend(BreakoutSigma1Factory().optimization(ohlcv, rough))       # BREAKOUT SIGMA1
        entry_strategies.extend(PercentRankerFactory().optimization(ohlcv, rough))        # PERCENT RANKER
        entry_strategies.extend(ThreeAmigosFactory().optimization(ohlcv, rough))          # THREE AMIGOS
        entry_strategies.extend(TwoAmigosFactory().optimization(ohlcv, rough))            # TWO AMIGOS
        # entry_strategies.extend(GoWithTheFlowFactory().optimization(ohlcv, rough))             # GO WITH THE FLOW
        # entry_strategies.extend(BooksCanBeGreatFactory().optimization(ohlcv, rough))       # BOOKS CAN BE GREAT
        # entry_strategies.extend(RSITriggerFactory().optimization(ohlcv, rough))       # RSI TRIGGER
        # entry_strategies.extend(MAWithTwistFactory().optimization(ohlcv, rough))       # MA WITH A TWIST
        # entry_strategies.extend(IntroducingSerialCorrelationFactory().optimization(ohlcv, rough))       # INTRO SERIAL
        # entry_strategies.extend(BackInStyleFactory().optimization(ohlcv, rough))       # BACK IN STYLE
        # entry_strategies.extend(ExponentiallyBetterFactory().optimization(ohlcv, rough))      # EXPONENTIALLY BETTER
        # entry_strategies.extend(StochasticCrossFactory().optimization(ohlcv, rough))      # STOCHASTIC CROSS
        # entry_strategies.extend(ShowMeTheMoneyFactory().optimization(ohlcv, rough))      # SHOW ME THE MONEY
        # entry_strategies.extend(ClassicBollingerbandsFactory().optimization(ohlcv, rough))      # CLASSIC BOLLINGERBANDS
        # entry_strategies.extend(ClassicKeltnerChannelFactory().optimization(ohlcv, rough))      # CLASSIC KC
        # entry_strategies.extend(PitterPatterPatternFactory().optimization(ohlcv, rough))        # PITTER PATTER PATTERN
        # entry_strategies.extend(PitterPatterPattern2Factory().optimization(ohlcv, rough))       # PITTER PATTER PATTERN2
        # entry_strategies.extend(ClosingPatternOnlyFactory().optimization(ohlcv, rough))       # CLOSING PATTERN ONLY
        # entry_strategies.extend(ClosingPatternOnly2Factory().optimization(ohlcv, rough))       # CLOSING PATTERN ONLY2
        # entry_strategies.extend(QuickPullbackPatternFactory().optimization(ohlcv, rough))       # QUICK PULLBACK PATTERN
        # entry_strategies.extend(BreakdownDeadAheadFactory().optimization(ohlcv, rough))       # BREAKDOWN DEAD A HEAD
        # entry_strategies.extend(EntryCommodityChannelIndexFactory().optimization(ohlcv, rough))    # ENTRY CCI
        # entry_strategies.extend(BigTailBarsFactory().optimization(ohlcv, rough))               # BIG TAIL BARS
        # entry_strategies.extend(NewHighWithConsecutiveHighsFactory().optimization(ohlcv, rough))   # NEW HIGH
        # entry_strategies.extend(StartWithAwesomeOscillatorFactory().optimization(ohlcv, rough))   # START AWESOME
        # entry_strategies.extend(SecondVerseSameAsTheFirstFactory().optimization(ohlcv, rough))   # SECOND VERSE
        # entry_strategies.extend(FilteredEntryFactory().optimization(ohlcv, rough))   # FILTERED ENTRY
        # entry_strategies.extend(TheUltimateFactory().optimization(ohlcv, rough))   # THE ULTIMATE
        # entry_strategies.extend(BreakoutKCFactory().optimization(ohlcv, rough))   # BREAKOUT KC
        # EXIT
        # 分足
        # exit_strategy = TimedByTimeFactory().create_strategy(ohlcv)                            # TIMED BY TIME
        # 日足
        # any
        # exit_strategy = NewvalueFactory().create_strategy(ohlcv)  # NEWVALUE
        # exit_strategy = TimedFactory().create_strategy(ohlcv)                            # TIMED
        # exit_strategy = ContractGainLossFactory().create_strategy(ohlcv)                   # CONTRACT GAIN AND LOSS
        # exit_strategy = PercentileFactory().create_strategy(ohlcv)                   # PERCENTILE
        # exit_strategy = GettingIsGoodFactory().create_strategy(ohlcv)                   # GETTING IS GOOD
        exit_strategy = EndOfBarFactory().create_strategy(ohlcv)                   # END OF BAR
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
        # 分足
        # entry_strategy = EconomicCalenderFactory().create_strategy(ohlcv)             # ECONOMIC CALENDER
        # entry_strategy = EnhancedEconomicCalenderFactory().create_strategy(ohlcv)     # ENHANCED ECONOMIC CALENDER
        # entry_strategy = IntradayBreakoutFactory().create_strategy(ohlcv)             # INTRADAY BREAKOUT
        # entry_strategy = IntradayBreakoutWithExpandingRangeFactory().create_strategy(ohlcv)  # INTRADAY BREAKOUT2
        # entry_strategy = ItsAboutTimeFactory().create_strategy(ohlcv)                 # IT'S ABOUT TIME
        # entry_strategy = RangeBreakoutFactory().create_strategy(ohlcv)                # RANGE BREAKOUT
        # entry_strategy = WhereYouAtFactory().create_strategy(ohlcv)                   # WHERE YOU AT
        # 日足
        # entry_strategy = DayOfWeekFactory().create_strategy(ohlcv)                    # DAY OF WEEK
        # entry_strategy = EveryoneLovesFridayFactory().create_strategy(ohlcv)          # EVERYONE LOVES FRIDAY
        # entry_strategy = SplitWeekFactory().create_strategy(ohlcv)                    # SPLIT WEEK
        # any
        # entry_strategy = BreakoutSigma1Factory().create_strategy(ohlcv)               # BREAKOUT SIGMA1
        # entry_strategy = GoWithTheFlowFactory().create_strategy(ohlcv)                # GO WITH THE FLOW
        # entry_strategy = BooksCanBeGreatFactory().create_strategy(ohlcv)              # BOOKS CAN BE GREAT
        # entry_strategy = BreakoutWithTwistFactory().create_strategy(ohlcv)            # BREAKOUT WITH A TWIST
        # entry_strategy = ATRBasedBreakoutFactory().create_strategy(ohlcv)             # ATR BASED BREAKOUT
        entry_strategy = BreakoutKCFactory().create_strategy(ohlcv)                   # BREAKOUT KC
        # entry_strategy = PercentRankerFactory().create_strategy(ohlcv)                # PERCENT RANKER
        # entry_strategy = RSITriggerFactory().create_strategy(ohlcv)                   # RSI TRIGGER
        # entry_strategy = MAWithTwistFactory().create_strategy(ohlcv)                  # MA WITH A TWIST
        # entry_strategy = IntroducingSerialCorrelationFactory().create_strategy(ohlcv) # INTRO SERIAL
        # entry_strategy = BackInStyleFactory().create_strategy(ohlcv)                  # BACK IN STYLE
        # entry_strategy = ExponentiallyBetterFactory().create_strategy(ohlcv)          # EXPONENTIALLY BETTER
        # entry_strategy = AsymmetricTripleFactory().create_strategy(ohlcv)             # ASYMMETRIC TRIPLE
        # entry_strategy = AsymmetricAgainFactory().create_strategy(ohlcv)              # ASYMMETRIC AGAIN
        # entry_strategy = StochasticCrossFactory().create_strategy(ohlcv)              # STOCHASTIC CROSS
        # entry_strategy = ShowMeTheMoneyFactory().create_strategy(ohlcv)               # SHOW ME THE MONEY
        # entry_strategy = ClassicBollingerbandsFactory().create_strategy(ohlcv)        # CLASSIC BOLLINGERBANDS
        # entry_strategy = ClassicKeltnerChannelFactory().create_strategy(ohlcv)        # CLASSIC KC
        # entry_strategy = ThreeAmigosFactory().create_strategy(ohlcv)                  # THREE AMIGOS
        # entry_strategy = TwoAmigosFactory().create_strategy(ohlcv)                    # TWO AMIGOS
        # entry_strategy = PitterPatterPatternFactory().create_strategy(ohlcv)          # PITTER PATTER PATTERN
        # entry_strategy = PitterPatterPattern2Factory().create_strategy(ohlcv)         # PITTER PATTER PATTERN2
        # entry_strategy = ClosingPatternOnlyFactory().create_strategy(ohlcv)           # CLOSING PATTERN ONLY
        # entry_strategy = ClosingPatternOnly2Factory().create_strategy(ohlcv)          # CLOSING PATTERN ONLY2
        # entry_strategy = QuickPullbackPatternFactory().create_strategy(ohlcv)         # QUICK PULLBACK PATTERN
        # entry_strategy = BreakdownDeadAheadFactory().create_strategy(ohlcv)           # BREAKDOWN DEAD A HEAD
        # entry_strategy = EntryCommodityChannelIndexFactory().create_strategy(ohlcv)   # ENTRY CCI
        # entry_strategy = BackInStyleFactory().create_strategy(ohlcv)                  # BIG TAIL BARS
        # entry_strategy = NewHighWithConsecutiveHighsFactory().create_strategy(ohlcv)  # NEW HIGH
        # entry_strategy = StartWithAwesomeOscillatorFactory().create_strategy(ohlcv)   # START AWESOME
        # entry_strategy = SecondVerseSameAsTheFirstFactory().create_strategy(ohlcv)    # SECOND VERSE
        # entry_strategy = FilteredEntryFactory().create_strategy(ohlcv)                # FILTERED ENTRY
        # entry_strategy = TheUltimateFactory().create_strategy(ohlcv)                  # THE ULTIMATE
        # EXIT
        # 分足
        # exit_strategies.extend(TimedFactory().optimization(ohlcv, rough))             # TIMED BY TIME
        # 日足
        # any
        # exit_strategies.extend(NewvalueFactory().optimization(ohlcv, rough))          # NEWVALUE
        exit_strategies.extend(TimedFactory().optimization(ohlcv, rough))             # TIMED
        # exit_strategies.extend(ContractGainLossFactory().optimization(ohlcv, rough))  # CONTRACT GAIN AND LOSS
        exit_strategies.extend(PercentileFactory().optimization(ohlcv, rough))        # PERCENTILE
        exit_strategies.extend(GettingIsGoodFactory().optimization(ohlcv, rough))     # GETTING IS GOOD
        # exit_strategies.extend(EndOfBarFactory().optimization(ohlcv, rough))          # END OF BAR
        # exit_strategies.extend(DontGiveItAllBackFactory().optimization(ohlcv, rough)) # DON'T GIVE IT ALL BACK
        # exit_strategies.extend(ProfitProtectorFactory().optimization(ohlcv, rough))   # PROFIT PROTECTOR
        # exit_strategies.extend(ExitWhereYouLikeFactory().optimization(ohlcv, rough))  # EXIT WHERE YOU LIKE
        # exit_strategies.extend(TieredFactory().optimization(ohlcv, rough))            # TIERED
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
    # symbol
    from lii3ra.symbol.volume_10b import Symbol
    symbol_list = Symbol.symbols

    # ashi
    ashi = "1d"
    # ashi = "15m"

    # range
    # start_date = "2010-01-01"
    start_date = "2004-01-01"
    end_date = "2019-12-31"

    # その他
    asset_values = {"initial_cash": 1000000, "leverage": 3.0, "losscut_ratio": 0.05}
    rough = False

    for symbol in symbol_list:
        combination_strategy(symbol, ashi, start_date, end_date, asset_values)
        # optimization_entry(symbol, ashi, start_date, end_date, asset_values, rough)
        # optimization_exit(symbol, ashi, start_date, end_date, asset_values, rough)


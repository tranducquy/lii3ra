#! /usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import numpy as np
import pandas as pd
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
from lii3ra.entry_strategy.breakout_sigma1_introserial import BreakoutSigma1IntroSerialFactory
from lii3ra.entry_strategy.peeling import PeelingFactory
from lii3ra.entry_strategy.peeling_stop import PeelingStopFactory
from lii3ra.entry_strategy.asymmetric_two_amigos import AsymmetricTwoAmigosFactory
from lii3ra.entry_strategy.breakout_kc import BreakoutKCFactory
from lii3ra.entry_strategy.asymmetric_again_with_flow import AsymmetricAgainWithFlowFactory
from lii3ra.entry_strategy.asymmetric_again_introserial import AsymmetricAgainIntroSerialFactory
from lii3ra.entry_strategy.atr_based_breakout_oneside import ATRBasedBreakoutOneSideFactory
# EXIT
from lii3ra.exit_strategy.newvalue import NewvalueFactory
from lii3ra.exit_strategy.lastvalue import LastValueFactory
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
from lii3ra.exit_strategy.sigma import SigmaFactory


s = Logger()
logger = s.myLogger()


def backtest(symbol
             , ashi
             , start_date
             , end_date
             , asset_values
             , entry_optimization=False
             , exit_optimization=False
             , resample=""):
    try:
        entry_strategies = []
        exit_strategies = []
        ohlcv = Ohlcv(symbol, ashi, start_date, end_date)
        if not resample == "":
            ohlcv.resample(resample)
            ashi = resample
        logger.info(f"backtest start[{entry_optimization},{exit_optimization}]")
        logger.info(f"parameter symbol={symbol}, ashi={ashi}, start_date={start_date}, end_date={end_date}")

        # ENTRY
        # 分足
        # entry_strategies.extend(EconomicCalenderFactory().create(ohlcv, entry_optimization))          # ECONOMIC CALENDER
        # entry_strategies.extend(EnhancedEconomicCalenderFactory().create(ohlcv, entry_optimization))  # ENHANCED ECONOMIC CALENDER
        # entry_strategies.extend(RangeBreakoutFactory().create(ohlcv, entry_optimization))             # RANGE BREAKOUT
        # entry_strategies.extend(IntradayBreakoutFactory().create(ohlcv, entry_optimization))          # INTRADAY BREAKOUT
        # entry_strategies.extend(IntradayBreakoutWithExpandingRangeFactory().create(ohlcv, entry_optimization))  # INTRADAY BREAKOUT2
        # entry_strategies.extend(ItsAboutTimeFactory().create(ohlcv, entry_optimization))              # IT'S ABOUT TIME
        # entry_strategies.extend(WhereYouAtFactory().create(ohlcv, entry_optimization))                # WHERE YOU AT
        # 日足
        # entry_strategies.extend(EveryoneLovesFridayFactory().create(ohlcv, entry_optimization))  # EVERYONE LOVES FRIDAY
        # entry_strategies.extend(SplitWeekFactory().create(ohlcv, entry_optimization))  # SPLIT WEEK
        # entry_strategies.extend(DayOfWeekFactory().create(ohlcv, entry_optimization))  # DAY OF WEEK
        # any
        # entry_strategies.extend(ATRBasedBreakoutFactory().create(ohlcv, entry_optimization))  # ATR BASED BREAKOUT
        # entry_strategies.extend(AsymmetricAgainFactory().create(ohlcv, entry_optimization))  # ASYMMETRIC AGAIN
        # entry_strategies.extend(AsymmetricTripleFactory().create(ohlcv, entry_optimization))  # ASYMMETRIC TRIPLE
        # entry_strategies.extend(BackInStyleFactory().create(ohlcv, entry_optimization))  # BACK IN STYLE
        # entry_strategies.extend(BigTailBarsFactory().create(ohlcv, entry_optimization))  # BIG TAIL BARS
        # entry_strategies.extend(BooksCanBeGreatFactory().create(ohlcv, entry_optimization))  # BOOKS CAN BE GREAT
        # entry_strategies.extend(BreakoutWithTwistFactory().create(ohlcv, entry_optimization))  # BREAKOUT WITH A TWIST
        entry_strategies.extend(BreakoutSigma1Factory().create(ohlcv, entry_optimization))  # BREAKOUT SIGMA1
        # entry_strategies.extend(TheUltimateFactory().create(ohlcv, entry_optimization))  # THE ULTIMATE
        # entry_strategies.extend(BreakdownDeadAheadFactory().create(ohlcv, entry_optimization))  # BREAKDOWN DEAD A HEAD
        # entry_strategies.extend(ClassicBollingerbandsFactory().create(ohlcv, entry_optimization))  # CLASSIC BOLLINGERBANDS
        # entry_strategies.extend(ClassicKeltnerChannelFactory().create(ohlcv, entry_optimization))  # CLASSIC KC
        # entry_strategies.extend(ClosingPatternOnlyFactory().create(ohlcv, entry_optimization))  # CLOSING PATTERN ONLY
        # entry_strategies.extend(ClosingPatternOnly2Factory().create(ohlcv, entry_optimization))  # CLOSING PATTERN ONLY2
        # entry_strategies.extend(EntryCommodityChannelIndexFactory().create(ohlcv, entry_optimization))  # ENTRY CCI
        # entry_strategies.extend(GoWithTheFlowFactory().create(ohlcv, entry_optimization))  # GO WITH THE FLOW
        # entry_strategies.extend(PercentRankerFactory().create(ohlcv, entry_optimization))  # PERCENT RANKER
        # entry_strategies.extend(RSITriggerFactory().create(ohlcv, entry_optimization))  # RSI TRIGGER
        # entry_strategies.extend(MAWithTwistFactory().create(ohlcv, entry_optimization))  # MA WITH A TWIST
        # entry_strategies.extend(IntroducingSerialCorrelationFactory().create(ohlcv, entry_optimization))  # INTRO SERIAL
        # entry_strategies.extend(ExponentiallyBetterFactory().create(ohlcv, entry_optimization))  # EXPONENTIALLY BETTER
        # entry_strategies.extend(StochasticCrossFactory().create(ohlcv, entry_optimization))  # STOCHASTIC CROSS
        # entry_strategies.extend(ShowMeTheMoneyFactory().create(ohlcv, entry_optimization))  # SHOW ME THE MONEY
        # entry_strategies.extend(PitterPatterPatternFactory().create(ohlcv, entry_optimization))  # PITTER PATTER PATTERN
        # entry_strategies.extend(PitterPatterPattern2Factory().create(ohlcv, entry_optimization))  # PITTER PATTER PATTERN2
        # entry_strategies.extend(QuickPullbackPatternFactory().create(ohlcv, entry_optimization))  # QUICK PULLBACK PATTERN
        # entry_strategies.extend(ThreeAmigosFactory().create(ohlcv, entry_optimization))  # THREE AMIGOS
        # entry_strategies.extend(TwoAmigosFactory().create(ohlcv, entry_optimization))  # TWO AMIGOS
        # entry_strategies.extend(NewHighWithConsecutiveHighsFactory().create(ohlcv, entry_optimization))  # NEW HIGH
        # entry_strategies.extend(StartWithAwesomeOscillatorFactory().create(ohlcv, entry_optimization))  # START AWESOME
        # entry_strategies.extend(SecondVerseSameAsTheFirstFactory().create(ohlcv, entry_optimization))  # SECOND VERSE
        # entry_strategies.extend(FilteredEntryFactory().create(ohlcv, entry_optimization))  # FILTERED ENTRY
        # entry_strategies.extend(BreakoutSigma1IntroSerialFactory().create(ohlcv, entry_optimization))  # BREAKOUT SIGMA1 INTRO
        # entry_strategies.extend(PeelingFactory().create(ohlcv, entry_optimization))                      # PEELING
        # entry_strategies.extend(PeelingStopFactory().create(ohlcv, entry_optimization))                      # PEELING STOP
        # entry_strategies.extend(AsymmetricTwoAmigosFactory().create(ohlcv, entry_optimization))            # ASYMMETRIC TWO AMIGOS
        entry_strategies.extend(BreakoutKCFactory().create(ohlcv, entry_optimization))          # BREAKOUT KC
        # entry_strategies.extend(AsymmetricAgainWithFlowFactory().create(ohlcv, entry_optimization))  # ASYMMETRIC AGAIN WITH FLOW
        # entry_strategies.extend(AsymmetricAgainIntroSerialFactory().create(ohlcv, entry_optimization))  # ASYMMETRIC AGAIN INTRO SERIAL
        # entry_strategies.extend(ATRBasedBreakoutOneSideFactory().create(ohlcv, entry_optimization))  # ATR BASED BREAKOUT ONE SIDE

        # EXIT
        # 分足
        # exit_strategies.extend(TimedFactory().optimization(ohlcv, rough))                       # TIMED BY TIME
        # 日足
        # any
        # exit_strategies.extend(NewvalueFactory().create(ohlcv, exit_optimization))              # NEWVALUE
        # exit_strategies.extend(LastValueFactory().create(ohlcv, exit_optimization))             # LASTVALUE
        # exit_strategies.extend(TimedFactory().create(ohlcv, exit_optimization))                 # TIMED
        # exit_strategies.extend(ContractGainLossFactory().create(ohlcv, exit_optimization))      # CONTRACT GAIN AND LOSS
        # exit_strategies.extend(PercentileFactory().create(ohlcv, exit_optimization))            # PERCENTILE
        # exit_strategies.extend(GettingIsGoodFactory().create(ohlcv, exit_optimization))         # GETTING IS GOOD
        exit_strategies.extend(EndOfBarFactory().create(ohlcv, exit_optimization))              # END OF BAR
        # exit_strategies.extend(DontGiveItAllBackFactory().create(ohlcv, exit_optimization))     # DON'T GIVE IT ALL BACK
        # exit_strategies.extend(ProfitProtectorFactory().create(ohlcv, exit_optimization))       # PROFIT PROTECTOR
        # exit_strategies.extend(ExitWhereYouLikeFactory().create(ohlcv, exit_optimization))      # EXIT WHERE YOU LIKE
        # exit_strategies.extend(TieredFactory().create(ohlcv, exit_optimization))                # TIERED
        # exit_strategies.extend(SigmaFactory().create(ohlcv, exit_optimization))                  # SIGMA
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


if __name__ == '__main__':
    # symbol
    # from lii3ra.symbol.tse1 import Symbol
    # from lii3ra.symbol.tse2 import Symbol
    # from lii3ra.symbol.tse2_100m import Symbol
    # from lii3ra.symbol.jasdaq import Symbol
    # from lii3ra.symbol.jasdaq_100m import Symbol
    # from lii3ra.symbol.mothers import Symbol
    # from lii3ra.symbol.mothers_100m import Symbol
    # from lii3ra.symbol.bollingerband_newvalue import Symbol
    # from lii3ra.symbol.topix17etf.topix17etf_nomura import Symbol
    # from lii3ra.symbol.n225 import Symbol
    # from lii3ra.symbol.n225_topix import Symbol
    # from lii3ra.symbol.yuusha_volume10b import Symbol
    # from lii3ra.symbol.volume_100m import Symbol
    # from lii3ra.symbol.topix17etf.volume1b.topix17etf_1617 import Symbol
    # from lii3ra.symbol.topix17etf.volume1b.topix17etf_1618 import Symbol
    # from lii3ra.symbol.topix17etf.volume1b.topix17etf_1619 import Symbol
    # from lii3ra.symbol.topix17etf.volume1b.topix17etf_1620 import Symbol
    # from lii3ra.symbol.topix17etf.volume1b.topix17etf_1621 import Symbol
    # from lii3ra.symbol.topix17etf.volume1b.topix17etf_1622 import Symbol
    # from lii3ra.symbol.topix17etf.volume1b.topix17etf_1623 import Symbol
    # from lii3ra.symbol.topix17etf.volume1b.topix17etf_1624 import Symbol
    # from lii3ra.symbol.topix17etf.volume1b.topix17etf_1625 import Symbol
    # from lii3ra.symbol.topix17etf.volume1b.topix17etf_1626 import Symbol
    # from lii3ra.symbol.topix17etf.volume1b.topix17etf_1627 import Symbol
    # from lii3ra.symbol.topix17etf.volume1b.topix17etf_1628 import Symbol
    # from lii3ra.symbol.topix17etf.volume1b.topix17etf_1630 import Symbol
    # from lii3ra.symbol.opt.atr2kc_20200122 import Symbol
    # from lii3ra.symbol.opt.average_day_range_2017_2019 import Symbol
    # import lii3ra.symbol.volume_100m
    # symbol_list = lii3ra.symbol.volume_100m.Symbol.symbols
    # import lii3ra.symbol.tse2_100m
    # import lii3ra.symbol.mothers_100m
    # import lii3ra.symbol.jasdaq_100m
    # symbol_list = lii3ra.symbol.tse2_100m.Symbol.symbols
    # symbol_list.extend(lii3ra.symbol.mothers_100m.Symbol.symbols)
    # symbol_list.extend(lii3ra.symbol.jasdaq_100m.Symbol.symbols)
    # symbol_list = ["^N225"]
    # symbol_list = ["Topix"]
    # symbol_list = ["Mothers"]
    # symbol_list = ["JPX400"]
    # symbol_list = ["DJI"]
    symbol_list = ["TREIT"]
    # symbol_list = ["N225minif"]
    # symbol_list = ["USDJPY", "GBPJPY", "EURJPY", "EURUSD", "EURUSD", "GBPUSD"]
    # symbol_list = ["9263.T"]

    # ashi
    ashi = "1d"
    resample = ""
    # range
    start_date = "2012-01-01"
    end_date = "2020-12-31"
    # 資産
    asset_values = {"initial_cash": 1000000, "leverage": 3.0, "losscut_ratio": 0.05}
    # 最適化
    entry_optimization = True
    exit_optimization = False

    for symbol in symbol_list:
        backtest(symbol, ashi, start_date, end_date, asset_values, entry_optimization, exit_optimization, resample)



#! /usr/bin/env python
# -*- coding: utf-8 -*-

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
# EXIT
from lii3ra.exit_strategy.newvalue import NewvalueFactory
from lii3ra.exit_strategy.timed import TimedFactory

# from lii3ra.symbol.test import Symbol
# from lii3ra.symbol.bollingerband_newvalue import Symbol
# from lii3ra.symbol.topix17etf_nomura import Symbol
# from lii3ra.symbol.n225 import Symbol
# from lii3ra.symbol.n225_topix import Symbol

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
        # entry_strategies.append(BreakoutSigma1Factory().create_strategy(ohlcv))           # BREAKOUT SIGMA1
        # entry_strategies.append(GoWithTheFlowFactory().create_strategy(ohlcv))            # GO WITH THE FLOW
        # entry_strategies.append(EveryoneLovesFridayFactory().create_strategy(ohlcv))        # EVERYONE LOVES FRIDAY
        # entry_strategies.append(BooksCanBeGreatFactory().create_strategy(ohlcv))        # BOOKS CAN BE GREAT
        # entry_strategies.append(BreakoutWithTwistFactory().create_strategy(ohlcv))        # BREAKOUT WITH A TWIST
        # entry_strategies.append(ATRBasedBreakoutFactory().create_strategy(ohlcv))         # ATR BASED BREAKOUT
        # entry_strategies.append(PercentRankerFactory().create_strategy(ohlcv))              # PERCENT RANKER
        # entry_strategies.append(RSITriggerFactory().create_strategy(ohlcv))        # RSI TRIGGER
        # entry_strategies.append(MAWithTwistFactory().create_strategy(ohlcv))        # MA WITH A TWIST
        # entry_strategies.append(SplitWeekFactory().create_strategy(ohlcv))        # SPLIT WEEK
        # entry_strategies.append(IntroducingSerialCorrelationFactory().create_strategy(ohlcv))        # INTRO SERIAL
        # entry_strategies.append(BackInStyleFactory().create_strategy(ohlcv))        # BACK IN STYLE
        # entry_strategies.append(WhereYouAtFactory().create_strategy(ohlcv))                # WHERE YOU AT
        # entry_strategies.append(ExponentiallyBetterFactory().create_strategy(ohlcv))       # EXPONENTIALLY BETTER
        # entry_strategies.append(AsymmetricTripleFactory().create_strategy(ohlcv))       # ASYMMETRIC TRIPLE
        # entry_strategies.append(AsymmetricAgainFactory().create_strategy(ohlcv))       # ASYMMETRIC AGAIN
        # entry_strategies.append(StochasticCrossFactory().create_strategy(ohlcv))       # STOCHASTIC CROSS
        # entry_strategies.append(ShowMeTheMoneyFactory().create_strategy(ohlcv))       # SHOW ME THE MONEY
        # entry_strategies.append(ClassicBollingerbandsFactory().create_strategy(ohlcv))       # CLASSIC BOLLINGERBANDS
        entry_strategies.append(ClassicKeltnerChannelFactory().create_strategy(ohlcv))       # CLASSIC KC
        # EXIT
        exit_strategies.append(NewvalueFactory().create_strategy(ohlcv))                  # NEWVALUE
        exit_strategies.append(TimedFactory().create_strategy(ohlcv))                     # TIMED
        for entry_strategy in entry_strategies:
            for exit_strategy in exit_strategies:
                asset = Asset(symbol
                              , asset_values["initial_cash"]
                              , asset_values["leverage"]
                              , asset_values["losscut_ratio"])
                Market().simulator_run(ohlcv, entry_strategy, exit_strategy, asset)
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
        # entry_strategies.extend(BreakoutSigma1Factory().optimization(ohlcv, rough))        # BREAKOUT SIGMA1
        # entry_strategies.extend(GoWithTheFlowFactory().optimization(ohlcv, rough))             # GO WITH THE FLOW
        # entry_strategies.extend(EveryoneLovesFridayFactory().optimization(ohlcv, rough))       # EVERYONE LOVES FRIDAY
        # entry_strategies.extend(BooksCanBeGreatFactory().optimization(ohlcv, rough))       # BOOKS CAN BE GREAT
        # entry_strategies.extend(BreakoutWithTwistFactory().optimization(ohlcv, rough))     # BREAKOUT WITH A TWIST
        # entry_strategies.extend(ATRBasedBreakoutFactory().optimization(ohlcv, rough))          # ATR BASED BREAKOUT
        # entry_strategies.extend(PercentRankerFactory().optimization(ohlcv, rough))             # PERCENT RANKER
        # entry_strategies.extend(RSITriggerFactory().optimization(ohlcv, rough))       # RSI TRIGGER
        # entry_strategies.extend(MAWithTwistFactory().optimization(ohlcv, rough))       # MA WITH A TWIST
        entry_strategies.extend(SplitWeekFactory().optimization(ohlcv, rough))       # SPLIT WEEK
        entry_strategies.extend(IntroducingSerialCorrelationFactory().optimization(ohlcv, rough))       # INTRO SERIAL
        entry_strategies.extend(BackInStyleFactory().optimization(ohlcv, rough))       # BACK IN STYLE
        entry_strategies.extend(WhereYouAtFactory().optimization(ohlcv, rough))               # WHERE YOU AT
        entry_strategies.extend(ExponentiallyBetterFactory().optimization(ohlcv, rough))      # EXPONENTIALLY BETTER
        entry_strategies.extend(AsymmetricTripleFactory().optimization(ohlcv, rough))      # ASTMETRIC TRIPLE
        entry_strategies.extend(AsymmetricAgainFactory().optimization(ohlcv, rough))      # ASTMETRIC AGAIN
        entry_strategies.extend(StochasticCrossFactory().optimization(ohlcv, rough))      # STOCHASTIC CROSS
        entry_strategies.extend(ShowMeTheMoneyFactory().optimization(ohlcv, rough))      # SHOW ME THE MONEY
        entry_strategies.extend(ClassicBollingerbandsFactory().optimization(ohlcv, rough))      # CLASSIC BOLLINGERBANDS
        entry_strategies.extend(ClassicKeltnerChannelFactory().optimization(ohlcv, rough))      # CLASSIC KC
        # EXIT
        exit_strategy = NewvalueFactory().create_strategy(ohlcv)                           # NEWVALUE
        # exit_strategy = TimedFactory().create_strategy(ohlcv)                            # TIMED
        for entry_strategy in entry_strategies:
            asset = Asset(symbol, asset_values["initial_cash"], asset_values["leverage"], asset_values["losscut_ratio"])
            Market().simulator_run(ohlcv, entry_strategy, exit_strategy, asset)
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
        # entry_strategy = BreakoutSigma1Factory().create_strategy(ohlcv)                 # BREAKOUT SIGMA1
        # entry_strategy = GoWithTheFlowFactory().create_strategy(ohlcv)                  # GO WITH THE FLOW
        # entry_strategy = EveryoneLovesFridayFactory().create_strategy(ohlcv)                  # EVERYONE LOVES FRIDAY
        # entry_strategy = BooksCanBeGreatFactory().create_strategy(ohlcv)                  # BOOKS CAN BE GREAT
        # entry_strategy = BreakoutWithTwistFactory().create_strategy(ohlcv)                # BREAKOUT WITH A TWIST
        # entry_strategy = ATRBasedBreakoutFactory().create_strategy(ohlcv)                 # ATR BASED BREAKOUT
        # entry_strategy = PercentRankerFactory().create_strategy(ohlcv)                 # PERCENT RANKER
        # entry_strategy = RSITriggerFactory().create_strategy(ohlcv)                  # RSI TRIGGER
        # entry_strategy = MAWithTwistFactory().create_strategy(ohlcv)                  # MA WITH A TWIST
        # entry_strategy = SplitWeekFactory().create_strategy(ohlcv)                  # SPLIT WEEK
        # entry_strategy = IntroducingSerialCorrelationFactory().create_strategy(ohlcv)     # INTRO SERIAL
        # entry_strategy = BackInStyleFactory().create_strategy(ohlcv)                    # BACK IN STYLE
        # entry_strategy = WhereYouAtFactory().create_strategy(ohlcv)                              # WHERE YOU AT
        # entry_strategy = ExponentiallyBetterFactory().create_strategy(ohlcv)                  # EXPONENTIALLY BETTER
        # entry_strategy = AsymmetricTripleFactory().create_strategy(ohlcv)                       # ASYMMETRIC TRIPLE
        # entry_strategy = AsymmetricAgainFactory().create_strategy(ohlcv)                       # ASYMMETRIC AGAIN
        # entry_strategy = StochasticCrossFactory().create_strategy(ohlcv)                       # STOCHASTIC CROSS
        # entry_strategy = ShowMeTheMoneyFactory().create_strategy(ohlcv)                       # SHOW ME THE MONEY
        # entry_strategy = ClassicBollingerbandsFactory().create_strategy(ohlcv)                # CLASSIC BOLLINGERBANDS
        entry_strategy = ClassicKeltnerChannelFactory().create_strategy(ohlcv)                  # CLASSIC KC
        # EXIT
        exit_strategies.extend(NewvalueFactory().optimization(ohlcv, rough))              # NEWVALUE
        exit_strategies.extend(TimedFactory().optimization(ohlcv, rough))                 # TIMED
        for exit_strategy in exit_strategies:
            asset = Asset(symbol, asset_values["initial_cash"], asset_values["leverage"], asset_values["losscut_ratio"])
            Market().simulator_run(ohlcv, entry_strategy, exit_strategy, asset)
    except Exception as err:
        print(err)
    logger.info("backtest bruteforce exit end")


if __name__ == '__main__':
    symbol = "^N225"
    # symbol = "6753.T"
    ashi = "1d"
    start_date = "2010-01-01"
    end_date = "2019-12-31"
    asset_values = {"initial_cash": 1000000, "leverage": 3.0, "losscut_ratio": 0.10}
    rough = True
    # rough = False
    combination_strategy(symbol, ashi, start_date, end_date, asset_values)
    # optimization_entry(symbol, ashi, start_date, end_date, asset_values, rough)
    # optimization_exit(symbol, ashi, start_date, end_date, asset_values, rough)



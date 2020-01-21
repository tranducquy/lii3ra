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
from lii3ra.entry_strategy.breakout_sigma1_introserial import BreakoutSigma1IntroSerialFactory
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


s = Logger()
logger = s.myLogger()


def swing_trading(symbol_list, ashi, start_date, end_date, asset_values):
    logger.info("backtest start")
    try:
        thread_pool = list()
        for symbol in symbol_list:
            logger.info(f"parameter symbol={symbol}, ashi={ashi}, start_date={start_date}, end_date={end_date}")
            ohlcv = Ohlcv(symbol, ashi, start_date, end_date)
            entry_list = None
            exit_list = None
            if "7717.T" == symbol:  # 電機・精密
                entry_list = BreakoutKCFactory().create(ohlcv)
                exit_list = PercentileFactory().create(ohlcv)
            elif "6753.T" == symbol:  # 電機・精密
                entry_list = BreakoutSigma1Factory().create(ohlcv)
                exit_list = NewvalueFactory().create(ohlcv)
            elif "3288.T" == symbol:  # 不動産
                entry_list = AsymmetricAgainFactory().create(ohlcv)
                exit_list = TimedFactory().create(ohlcv)
            elif "3038.T" == symbol:  # 商社・卸
                entry_list = AsymmetricAgainFactory().create(ohlcv)
                exit_list = GettingIsGoodFactory().create(ohlcv)
            elif "7974.T" == symbol:  # 情報通信サービス・その他
                entry_list = AsymmetricTripleFactory().create(ohlcv)
                exit_list = NewvalueFactory().create(ohlcv)
            elif '1568.T' == symbol:  # [x] ETF
                entry_list = BreakoutSigma1Factory().create(ohlcv)
                exit_list = GettingIsGoodFactory().create(ohlcv)
            elif '1802.T' == symbol:  # [x] 建設
                entry_list = AsymmetricAgainFactory().create(ohlcv)
                exit_list = DontGiveItAllBackFactory().create(ohlcv)
            elif '2503.T' == symbol:  # [x] 食品
                entry_list = BreakoutWithTwistFactory().create(ohlcv)
                exit_list = ContractGainLossFactory().create(ohlcv)
            elif '3141.T' == symbol:  # [x] 小売
                entry_list = AsymmetricAgainFactory().create(ohlcv)
                exit_list = TimedFactory().create(ohlcv)
            elif '8267.T' == symbol:  # [x] 小売
                entry_list = AsymmetricAgainFactory().create(ohlcv)
                exit_list = TimedFactory().create(ohlcv)
            elif '9983.T' == symbol:  # [x] 小売
                entry_list = AsymmetricAgainFactory().create(ohlcv)
                exit_list = PercentileFactory().create(ohlcv)
            elif '4911.T' == symbol:  # [x] 素材・化学
                entry_list = AsymmetricAgainFactory().create(ohlcv)
                exit_list = NewvalueFactory().create(ohlcv)
            elif '4967.T' == symbol:  # [x] 素材・化学
                entry_list = AsymmetricAgainFactory().create(ohlcv)
                exit_list = ContractGainLossFactory().create(ohlcv)
            elif '4523.T' == symbol:  # [x] 医薬品
                entry_list = AsymmetricAgainFactory().create(ohlcv)
                exit_list = GettingIsGoodFactory().create(ohlcv)
            elif '5411.T' == symbol:  # [x] 製鋼・非鉄
                entry_list = ATRBasedBreakoutFactory().create(ohlcv)
                exit_list = NewvalueFactory().create(ohlcv)
            elif '5706.T' == symbol:  # [x] 製鋼・非鉄
                entry_list = BreakoutKCFactory().create(ohlcv)
                exit_list = TimedFactory().create(ohlcv)
            elif '5713.T' == symbol:  # [x] 製鋼・非鉄
                entry_list = AsymmetricAgainFactory().create(ohlcv)
                exit_list = TimedFactory().create(ohlcv)
            elif '2412.T' == symbol:  # [x] 情報通信サービス・その他
                entry_list = AsymmetricAgainFactory().create(ohlcv)
                exit_list = ContractGainLossFactory().create(ohlcv)
            elif '2427.T' == symbol:  # [x] 情報通信サービス・その他
                entry_list = RSITriggerFactory().create(ohlcv)
                exit_list = NewvalueFactory().create(ohlcv)
            elif '6047.T' == symbol:  # [x] 情報通信サービス・その他
                entry_list = TwoAmigosFactory().create(ohlcv)
                exit_list = TimedFactory().create(ohlcv)
            elif '8876.T' == symbol:  # [x] 情報通信サービス・その他
                entry_list = AsymmetricAgainFactory().create(ohlcv)
                exit_list = GettingIsGoodFactory().create(ohlcv)
            elif '9424.T' == symbol:  # [x] 情報通信サービス・その他
                entry_list = PercentRankerFactory().create(ohlcv)
                exit_list = ContractGainLossFactory().create(ohlcv)
            elif '9616.T' == symbol:  # [x] 情報通信サービス・その他
                entry_list = TwoAmigosFactory().create(ohlcv)
                exit_list = LastValueFactory().create(ohlcv)
            elif '6141.T' == symbol:  # [x] 機械
                entry_list = BreakoutSigma1Factory().create(ohlcv)
                exit_list = NewvalueFactory().create(ohlcv)
            elif '6473.T' == symbol:  # [x] 機械
                entry_list = StochasticCrossFactory().create(ohlcv)
                exit_list = ContractGainLossFactory().create(ohlcv)
            elif '6479.T' == symbol:  # [x] 電機・精密
                entry_list = BreakoutKCFactory().create(ohlcv)
                exit_list = PercentileFactory().create(ohlcv)
            elif '6619.T' == symbol:  # [x] 電機・精密
                entry_list = TheUltimateFactory().create(ohlcv)
                exit_list = EndOfBarFactory().create(ohlcv)
            elif '6762.T' == symbol:  # [x] 電機・精密
                entry_list = PercentRankerFactory().create(ohlcv)
                exit_list = TimedFactory().create(ohlcv)
            elif '6920.T' == symbol:  # [x] 電機・精密
                entry_list = BreakoutKCFactory().create(ohlcv)
                exit_list = ContractGainLossFactory().create(ohlcv)
            elif '8306.T' == symbol:  # [x] 銀行
                entry_list = ATRBasedBreakoutFactory().create(ohlcv)
                exit_list = DontGiveItAllBackFactory().create(ohlcv)
            elif '9007.T' == symbol:  # [x] 運輸・物流
                entry_list = AsymmetricTripleFactory().create(ohlcv)
                exit_list = TimedFactory().create(ohlcv)
            elif '3088.T' == symbol:  # [x] 小売
                entry_list = TheUltimateFactory().create(ohlcv)
                exit_list = GettingIsGoodFactory().create(ohlcv)
            elif "1570.T" == symbol:  # ETF
                entry_list = ATRBasedBreakoutFactory().create(ohlcv)
                exit_list = NewvalueFactory().create(ohlcv)
            elif '9104.T' == symbol:  # 海運
                entry_list = BreakoutSigma1Factory().create(ohlcv)
                exit_list = NewvalueFactory().create(ohlcv)
            elif '9107.T' == symbol:  # 海運
                entry_list = ATRBasedBreakoutFactory().create(ohlcv)
                exit_list = NewvalueFactory().create(ohlcv)
            elif "^N225" == symbol:
                entry_list = ATRBasedBreakoutFactory().create(ohlcv)
                exit_list = EndOfBarFactory().create(ohlcv)
            elif "Topix" == symbol:
                entry_list = BreakoutSigma1Factory().create(ohlcv)
                exit_list = NewvalueFactory().create(ohlcv)
            elif "Mothers" == symbol:
                entry_list = ATRBasedBreakoutFactory().create(ohlcv)
                exit_list = EndOfBarFactory().create(ohlcv)
            elif "JPX400" == symbol:
                entry_list = ATRBasedBreakoutFactory().create(ohlcv)
                exit_list = EndOfBarFactory().create(ohlcv)
            elif "4043.T" == symbol:
                entry_list = ATRBasedBreakoutFactory().create(ohlcv)
                exit_list = EndOfBarFactory().create(ohlcv)
            elif "3064.T" == symbol:
                entry_list = ATRBasedBreakoutFactory().create(ohlcv)
                exit_list = EndOfBarFactory().create(ohlcv)
            elif "2267.T" == symbol:
                entry_list = ATRBasedBreakoutFactory().create(ohlcv)
                exit_list = EndOfBarFactory().create(ohlcv)
            for entry_strategy in entry_list:
                for exit_strategy in exit_list:
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
    from lii3ra.symbol.yuusha_volume10b import Symbol
    symbol_list = Symbol.symbols
    temp_list = [
                    "1570.T"
                    , "9107.T"
                    , "9104.T"
                    , "^N225"
                    , "Topix"
                    , "Mothers"
    ]
    symbol_list.extend(temp_list)
    # ashi
    ashi = "1d"
    # range
    start_date = "2012-01-01"
    end_date = "2020-12-31"
    # その他
    asset_values = {"initial_cash": 1000000, "leverage": 3.0, "losscut_ratio": 0.05}
    swing_trading(symbol_list, ashi, start_date, end_date, asset_values)


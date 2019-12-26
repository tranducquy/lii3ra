# -*- coding: utf-8 -*-

from datetime import datetime
import numpy as np
from lii3ra.mylogger import Logger
from lii3ra.dbaccess import DbAccess


class BacktestDumper():
    def __init__(self, logger=None):
        if logger is None:
            self.logger = Logger().myLogger()
        else:
            self.logger = logger

    def save_simulate_result(
            self
            , symbol
            , leg
            , entry_strategy_title
            , exit_strategy_title
            , start_time
            , end_time
            , market_start_time
            , market_end_time
            , initial_assets
            , last_assets
            , rate_of_return
            , win_count
            , loss_count
            , win_value
            , loss_value
            , win_rate
            , payoffratio
            , profit_rate_per_trade
            , long_win_count
            , long_loss_count
            , long_win_value
            , long_loss_value
            , long_win_rate
            , long_payoffratio
            , long_profit_rate_per_trade
            , short_win_count
            , short_loss_count
            , short_win_value
            , short_loss_value
            , short_win_rate
            , short_payoffratio
            , short_profit_rate_per_trade
            , fee
            , spread_fee
            , regist_time
    ):
        params = {
            'symbol': symbol
            , 'leg': leg
            , 'entry_strategy': entry_strategy_title
            , 'exit_strategy': exit_strategy_title
            , 'start_time': start_time
            , 'end_time': end_time
            , 'market_start_time': market_start_time
            , 'market_end_time': market_end_time
            , 'initial_assets': initial_assets
            , 'last_assets': last_assets
            , 'rate_of_return': rate_of_return
            , 'win_count': win_count
            , 'loss_count': loss_count
            , 'win_value': win_value
            , 'loss_value': loss_value
            , 'win_rate': win_rate
            , 'payoffratio': payoffratio
            , 'profit_rate_per_trade': profit_rate_per_trade
            , 'long_win_count': long_win_count
            , 'long_loss_count': long_loss_count
            , 'long_win_value': long_win_value
            , 'long_loss_value': long_loss_value
            , 'long_win_rate': long_win_rate
            , 'long_payoffratio': long_payoffratio
            , 'long_profit_rate_per_trade': long_profit_rate_per_trade
            , 'short_win_count': short_win_count
            , 'short_loss_count': short_loss_count
            , 'short_win_value': short_win_value
            , 'short_loss_value': short_loss_value
            , 'short_win_rate': short_win_rate
            , 'short_payoffratio': short_payoffratio
            , 'short_profit_rate_per_trade': short_profit_rate_per_trade
            , 'fee': fee
            , 'spread_fee': spread_fee
            , 'regist_time': regist_time
        }
        dba = DbAccess()
        dba.delete_backtest_result(symbol, leg, entry_strategy_title, exit_strategy_title)
        dba.insert_backtest_result(params)

    def _check_float(self, num):
        if num is None or np.isnan(num):
            return 0.00
        else:
            return float(num)

    def make_history(
            self
            , ohlcv
            , entry_strategy_title
            , exit_strategy_title
            , idx
            , order_info
            , call_order_info
            , execution_order_info
            , execution_order_info2
            , position
            , asset
            , total_value
            , trade_performance
            , entry_indicators
            , entry_vol_indicators
            , exit_indicators
    ):
        if 'volume' in ohlcv.values:
            vol = float(ohlcv.values['volume'][idx])
        else:
            vol = 0.00
        t = (
            ohlcv.symbol
            , ohlcv.ashi
            , entry_strategy_title
            , exit_strategy_title
            , ohlcv.values['time'][idx]
            , self.round(self._check_float(ohlcv.values['open'][idx]))
            , self.round(self._check_float(ohlcv.values['high'][idx]))
            , self.round(self._check_float(ohlcv.values['low'][idx]))
            , self.round(self._check_float(ohlcv.values['close'][idx]))
            , vol
            # entry_indicator
            , self.round(self._check_float(entry_indicators[0]))
            , self.round(self._check_float(entry_indicators[1]))
            , self.round(self._check_float(entry_indicators[2]))
            , self.round(self._check_float(entry_indicators[3]))
            , self.round(self._check_float(entry_indicators[4]))
            , self.round(self._check_float(entry_indicators[5]))
            , self.round(self._check_float(entry_indicators[6]))
            # exit_indicator
            , self.round(self._check_float(exit_indicators[0]))
            , self.round(self._check_float(exit_indicators[1]))
            , self.round(self._check_float(exit_indicators[2]))
            , self.round(self._check_float(exit_indicators[3]))
            , self.round(self._check_float(exit_indicators[4]))
            , self.round(self._check_float(exit_indicators[5]))
            , self.round(self._check_float(exit_indicators[6]))
            # entry_vol_indicator
            , self.round(self._check_float(entry_vol_indicators[0]))
            , self.round(self._check_float(entry_vol_indicators[1]))
            , self.round(self._check_float(entry_vol_indicators[2]))
            , self.round(self._check_float(entry_vol_indicators[3]))
            , self.round(self._check_float(entry_vol_indicators[4]))
            , order_info['create_time']
            , order_info['order_type']
            , self.round(self._check_float(order_info['vol']))
            , self.round(self._check_float(order_info['price']))
            , call_order_info['order_time']
            , call_order_info['order_type']
            , self.round(self._check_float(call_order_info['vol']))
            , self.round(self._check_float(call_order_info['price']))
            , execution_order_info['exit_order_time']
            , execution_order_info['order_type']
            , execution_order_info['order_status']
            , self.round(self._check_float(execution_order_info['vol']))
            , self.round(self._check_float(execution_order_info['price']))
            , execution_order_info2['exit_order_time']
            , execution_order_info2['order_type']
            , execution_order_info2['order_status']
            , self.round(self._check_float(execution_order_info2['vol']))
            , self.round(self._check_float(execution_order_info2['price']))
            , position.position
            , self.round(self._check_float(asset.cash))
            , self.round(self._check_float(position.pos_vol))
            , self.round(self._check_float(position.pos_price))
            , self.round(self._check_float(total_value))
            , self.round(self._check_float(trade_performance['profit_value']))
            , self.round(self._check_float(trade_performance['profit_rate']))
            , self.round(self._check_float(trade_performance['fee']))
            , self.round(self._check_float(trade_performance['spread_fee']))
            , self.round(asset.leverage)
        )
        return t

    def save_history(self, symbol, ashi, entry_strategy, exit_strategy, backtest_history):
        dba = DbAccess()
        dba.delete_backtest_history(symbol, ashi, entry_strategy, exit_strategy)
        dba.insert_backtest_history(backtest_history)

    def save_result(self, entry_strategy_title, exit_strategy_title, summary, ohlcv):
        if ohlcv.values.index.size == 0:
            return "\n"
        if summary['WinCount'] == 0 and summary['LoseCount'] == 0:
            win_rate = 0
        else:
            win_rate = self.round(summary['WinCount'] / (summary['WinCount'] + summary['LoseCount']) * 100)
        if summary['LongWinCount'] == 0 and summary['LongLoseCount'] == 0:
            long_win_rate = 0
        else:
            long_win_rate = self.round(
                summary['LongWinCount'] / (summary['LongWinCount'] + summary['LongLoseCount']) * 100)
        if summary['ShortWinCount'] == 0 and summary['ShortLoseCount'] == 0:
            short_win_rate = 0
        else:
            short_win_rate = self.round(
                summary['ShortWinCount'] / (summary['ShortWinCount'] + summary['ShortLoseCount']) * 100)
        if summary['WinCount'] == 0 or summary['LoseCount'] == 0:
            payoffratio = 0
        else:
            payoffratio = self.round(
                (summary['WinValue'] / summary['WinCount']) / (summary['LoseValue'] / summary['LoseCount']))
        if summary['LongWinCount'] == 0 or summary['LongLoseCount'] == 0 or summary['LongWinValue'] == 0 or summary[
            'LongLoseValue'] == 0:
            long_payoffratio = 0
        else:
            long_payoffratio = self.round((summary['LongWinValue'] / summary['LongWinCount']) / (
                        summary['LongLoseValue'] / summary['LongLoseCount']))
        if summary['ShortWinCount'] == 0 or summary['ShortLoseCount'] == 0 or summary['ShortWinValue'] == 0 or summary[
            'ShortLoseValue'] == 0:
            short_payoffratio = 0
        else:
            short_payoffratio = self.round((summary['ShortWinValue'] / summary['ShortWinCount']) / (
                        summary['ShortLoseValue'] / summary['ShortLoseCount']))
        if summary['InitValue'] == 0:
            rate_of_return = 0
        else:
            rate_of_return = self.round((summary['LastValue'] - summary['InitValue']) / summary['InitValue'] * 100)
        if summary['WinCount'] == 0 and summary['LoseCount'] == 0:
            profit_rate_per_trade = 0
        else:
            profit_rate_per_trade = self.round(
                summary['ProfitRateSummary'] / (summary['WinCount'] + summary['LoseCount']))
        if summary['LongWinCount'] == 0 and summary['LongLoseCount'] == 0:
            long_profit_rate_per_trade = 0
        else:
            long_profit_rate_per_trade = self.round(
                summary['LongProfitRateSummary'] / (summary['LongWinCount'] + summary['LongLoseCount']))
        if summary['ShortWinCount'] == 0 and summary['ShortLoseCount'] == 0:
            short_profit_rate_per_trade = 0
        else:
            short_profit_rate_per_trade = self.round(
                summary['ShortProfitRateSummary'] / (summary['ShortWinCount'] + summary['ShortLoseCount']))
        if summary['PositionHavingSec'] == 0 and (summary['WinCount'] + summary['LoseCount']) == 0:
            position_having_sec_per_trade = 0
        else:
            position_having_sec_per_trade = self.round(
                summary['PositionHavingSec'] / (summary['WinCount'] + summary['LoseCount']))
        symbol = ohlcv.symbol
        start_date = ohlcv.start_date
        end_date = ohlcv.end_date
        ashi = ohlcv.ashi
        market_start_time = ohlcv.get_headdate()
        market_end_time = ohlcv.get_taildate()
        regist_time = datetime.now()
        msg = f"{symbol}"
        msg += f",{ashi}"
        # msg += f",バックテスト開始日:{start_date}"
        # msg += f",バックテスト終了日:{end_date}"
        market_start_date = market_start_time.strftime("%Y%m%d")
        msg += f",取引開始日時:{market_start_date}"
        market_end_date = market_end_time.strftime("%Y%m%d")
        msg += f",取引終了日時:{market_end_date}"
        msg += f",トレード保有秒数:{summary['PositionHavingSec']}"
        msg += f",1トレードあたりの平均日数:{position_having_sec_per_trade}"
        msg += f",初期資産:{summary['InitValue']:.0f}"
        msg += f",最終資産:{summary['LastValue']:.0f}"
        msg += f",全体騰落率(%%):{rate_of_return:.2f}"
        msg += f",勝ちトレード数:{summary['WinCount']:.0f}"
        msg += f",負けトレード数:{summary['LoseCount']:.0f}"
        msg += f",勝率(%%):{win_rate:.4f}"
        msg += f",ペイオフレシオ:{payoffratio:.4f}"
        msg += f",1トレードあたりの利益率(%%):{profit_rate_per_trade:.4f}"
        msg += f",1トレードあたりの利益率long(%%):{long_profit_rate_per_trade:.4f}"
        msg += f",1トレードあたりの利益率short(%%):{short_profit_rate_per_trade:.4f}"
        msg += f",売買手数料:{summary['Fee']:.2f}"
        msg += f",スプレッドによる差損:{summary['SpreadFee']:.4f}"
        msg += f",{entry_strategy_title}"
        msg += f",{exit_strategy_title}"
        # dbに保存
        self.save_simulate_result(
            symbol
            , ashi
            , entry_strategy_title
            , exit_strategy_title
            , start_date
            , end_date
            , market_start_time
            , market_end_time
            , summary['InitValue']
            , summary['LastValue']
            , self.round(rate_of_return)
            , summary['WinCount']
            , summary['LoseCount']
            , summary['WinValue']
            , summary['LoseValue']
            , self.round(win_rate)
            , self.round(payoffratio)
            , self.round(profit_rate_per_trade)
            , summary['LongWinCount']
            , summary['LongLoseCount']
            , summary['LongWinValue']
            , summary['LongLoseValue']
            , self.round(long_win_rate)
            , self.round(long_payoffratio)
            , self.round(long_profit_rate_per_trade)
            , summary['ShortWinCount']
            , summary['ShortLoseCount']
            , summary['ShortWinValue']
            , summary['ShortLoseValue']
            , self.round(short_win_rate)
            , self.round(short_payoffratio)
            , self.round(short_profit_rate_per_trade)
            , self.round(summary['Fee'])
            , self.round(summary['SpreadFee'])
            , regist_time
        )
        return msg

    def update_maxdrawdown(self, symbol, leg, entry_strategy, exit_strategy, start_date, end_date):
        # ドローダウン算出
        drawdown = self.get_maxdrawdown(symbol, leg, entry_strategy, exit_strategy, start_date, end_date)
        # DB更新
        dba = DbAccess()
        dba.update_maxdrawdown(symbol, leg, entry_strategy, exit_strategy, drawdown)

    def get_maxdrawdown(self
                        , symbol
                        , leg
                        , entry_strategy
                        , exit_strategy
                        , start_date
                        , end_date
                        ):
        dba = DbAccess()
        rs = dba.get_backtest_history(symbol, leg, entry_strategy, exit_strategy, start_date, end_date)
        maxv = 0
        minv = 0
        max_drawdown = 0
        c_time = ''
        count = 0
        if rs:
            for r in rs:
                v = r[1] + (r[2] * r[3])
                if count == 0:
                    maxv = v
                    minv = v
                elif maxv < v:
                    maxv = v
                    minv = v
                elif minv > v:
                    minv = v
                    diff = maxv - minv
                    drawdown = self.round(diff / maxv)
                    if max_drawdown < drawdown:
                        max_drawdown = drawdown
                        c_time = r[0]
                count += 1
            # self.logger.info(
            #    f"maxdrawdown:{symbol},{leg},{entry_strategy},{exit_strategy}"\
            #    f",{start_date},{end_date},{c_time},{max_drawdown}")
        return max_drawdown

    def round(self, v):
        return round(v, 4)

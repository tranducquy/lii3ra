# -*- coding: utf-8 -*-

import psycopg2
from psycopg2.extensions import AsIs
import pandas as pd
from lii3ra.mylogger import Logger
from lii3ra.dbinfo import DbInfo


class DbAccess:
    def __init__(self, l=None, dsn=None):
        if l is None:
            self.logger = Logger().myLogger()
        else:
            self.logger = l
        if dsn is None:
            self.dsn = 'postgresql://{username}:{password}@{hostname}:{port}/{database}'.format(
                username=DbInfo.USER_NAME
                , password=DbInfo.PASSWORD
                , hostname=DbInfo.HOSTNAME
                , port=DbInfo.PORT
                , database=DbInfo.DATABASE
            )
        else:
            self.dsn = dsn

    def connect_db(self):
        """Connects to the specific database."""
        return psycopg2.connect(self.dsn)

    def get_db(self):
        """Opens a new database connection if there is none yet for the
        current application context.
        """
        if not hasattr(self, 'db'):
            self.db = self.connect_db()
        return self.db

    def close_db(self, error):
        """Closes the database again at the end of the request."""
        if hasattr(self, 'db'):
            self.db.close()

    def get_maxtime_from_ohlcv(self, symbol, ashi):
        try:
            conn = self.get_db()
            c = conn.cursor()
            # ohlcの最終登録日を取得
            c.execute("""
                    select
                    max(time)
                    from ohlcv
                    where symbol ='{0}'""".format(symbol))
            max_time = c.fetchone()
        except Exception as err:
            self.logger.error('error dayo. {0}'.format(err))
        finally:
            if conn:
                conn.close()
        if max_time:
            return max_time[0]
        else:
            return None

    def get_ohlcv(self, symbol, ashi, start_date, end_date):
        try:
            conn = self.get_db()
            df = pd.read_sql("""select
                                      symbol
                                     , leg
                                     , time
                                     , open
                                     , high
                                     , low
                                     , close
                                     , volume
                                     from ohlcv
                                     where symbol = '%s'
                                     and leg = '%s'
                                     and time between '%s' and '%s'
                                     --and substr(text(time), 12,8) between '09:00:00' and '15:00:00'
                                     --and substr(text(time), 12,8) between '08:00:00' and '11:30:00'
                                     order by time 
                                     """
                             % (
                                 symbol
                                 , ashi
                                 , start_date
                                 , end_date
                             ), con=conn)
        except Exception as err:
            self.logger.error('error dayo. {0}'.format(err))
        finally:
            if conn:
                conn.close()
        return df

    def insert_backtest_result(self, params):
        try:
            conn = self.get_db()
            cur = conn.cursor()
            columns = list(params.keys())
            values = [params[column] for column in columns]
            insert_statement = "insert into backtest_result (%s) values %s"
            cur.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
        except Exception as err:
            self.logger.error('error dayo. {0}'.format(err))
            if cur and conn:
                conn.rollback()
        finally:
            if cur and conn:
                conn.commit()
                cur.close()
                conn.close()

    def delete_backtest_result(self, symbol, ashi, entry_strategy, exit_strategy):
        try:
            conn = self.get_db()
            cur = conn.cursor()
            values = [symbol, ashi, entry_strategy, exit_strategy]
            delete_statement = """
                                delete from backtest_result 
                                where symbol = %s
                                and leg = %s
                                and entry_strategy = %s
                                and exit_strategy = %s
                                """
            cur.execute(delete_statement, tuple(values))
        except Exception as err:
            self.logger.error('error dayo. {0}'.format(err))
            if cur and conn:
                conn.rollback()
        finally:
            if cur and conn:
                conn.commit()
                cur.close()

    def insert_backtest_history(self, history):
        try:
            conn = self.get_db()
            cur = conn.cursor()
            cur.executemany("""
                        insert into backtest_history
                        (
                         symbol
                        ,leg
                        ,entry_strategy
                        ,exit_strategy
                        ,time
                        ,open
                        ,high
                        ,low
                        ,close
                        ,volume
                        ,entry_indicator1
                        ,entry_indicator2
                        ,entry_indicator3
                        ,entry_indicator4
                        ,entry_indicator5
                        ,entry_indicator6
                        ,entry_indicator7
                        ,exit_indicator1
                        ,exit_indicator2
                        ,exit_indicator3
                        ,exit_indicator4
                        ,exit_indicator5
                        ,exit_indicator6
                        ,exit_indicator7
                        ,vol_indicator1
                        ,vol_indicator2
                        ,vol_indicator3
                        ,vol_indicator4
                        ,vol_indicator5
                        ,order_create_time 
                        ,order_type
                        ,order_vol
                        ,order_price
                        ,call_order_time
                        ,call_order_type
                        ,call_order_vol
                        ,call_order_price
                        ,execution_order_time
                        ,execution_order_type
                        ,execution_order_status
                        ,execution_order_vol
                        ,execution_order_price
                        ,execution_order_time2
                        ,execution_order_type2
                        ,execution_order_status2
                        ,execution_order_vol2
                        ,execution_order_price2
                        ,position
                        ,cash
                        ,pos_vol
                        ,pos_price
                        ,total_value
                        ,profit_value
                        ,profit_rate
                        ,fee
                        ,spread_fee
                        ,leverage
                        ,regist_time
                        ,max_drawdown
                        )
                        values
                        ( 
                         %s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,%s
                        ,current_timestamp
                        ,%s
                        )
                    """,
                            history
                            )
        except Exception as err:
            if conn:
                conn.rollback()
                self.logger.error(err)
        finally:
            if conn:
                conn.commit()
                conn.close

    def delete_backtest_history(self, symbol, ashi, entry_strategy, exit_strategy):
        try:
            conn = self.get_db()
            cur = conn.cursor()
            values = [symbol, ashi, entry_strategy, exit_strategy]
            delete_statement = """
                                delete from backtest_history
                                where symbol = %s
                                and leg = %s
                                and entry_strategy = %s
                                and exit_strategy = %s
                                """
            cur.execute(delete_statement, tuple(values))
        except Exception as err:
            self.logger.error('error dayo. {0}'.format(err))
            if cur and conn:
                conn.rollback()
        finally:
            if cur and conn:
                conn.commit()
                cur.close()
                # conn.close()

    def get_backtest_history(self, symbol, leg, entry_strategy, exit_strategy, start_date, end_date):
        try:
            conn = self.get_db()
            cur = conn.cursor()
            cur.execute(f"""
                        select
                         time
                        ,cash
                        ,pos_price
                        ,pos_vol 
                        from backtest_history 
                        where symbol = '{symbol}'
                        and leg = '{leg}'
                        and entry_strategy = '{entry_strategy}'
                        and exit_strategy = '{exit_strategy}'
                        and date(time) between '{start_date}' and '{end_date}'
                        order by time
                    """)
            rs = cur.fetchall()
        except Exception as err:
            self.logger.error('error dayo. {0}'.format(err))
        finally:
            if cur and conn:
                conn.close()
        return rs

    def update_maxdrawdown(self, symbol, ashi, entry_strategy, exit_strategy, drawdown):
        try:
            conn = self.get_db()
            cur = conn.cursor()
            cur.execute(f"""
                        update backtest_result set 
                        max_drawdown = {drawdown} 
                        where symbol = '{symbol}'
                        and leg = '{ashi}'
                        and entry_strategy = '{entry_strategy}'
                        and exit_strategy = '{exit_strategy}'
                        """)
            # self.logger.info(f"update_drawdown() {symbol},{ashi},{entry_strategy},{exit_strategy}")
        except Exception as err:
            self.logger.error('error dayo. {0}'.format(err))
            if cur and conn:
                conn.rollback()
        finally:
            if cur and conn:
                conn.commit()
                cur.close()
                conn.close()

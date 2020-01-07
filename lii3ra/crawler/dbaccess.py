# -*- coding: utf-8 -*-

import psycopg2
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

    def _convert_tomany(self, quotes):
        datalist = []
        for q in quotes:
            datalist.append([
                q[0]
                , q[1]
                , q[2]
                , q[3]
                , q[4]
                , q[5]
                , q[6]
                , q[7]
                , q[3]
                , q[4]
                , q[5]
                , q[6]
                , q[7]
            ]
            )
        return datalist

    def insert_ohlcv(self, quotes):
        try:
            record_count = len(quotes)
            self.logger.info("insert_ohlcv() start. {0}".format(record_count))
            conn = self.get_db()
            c = conn.cursor()
            q = self._convert_tomany(quotes)
            query = """INSERT INTO ohlcv 
                        (symbol, leg, time, open, high, low, close, volume) 
                       VALUES
                        (%s,%s,%s,%s,%s,%s,%s,%s) 
                       ON CONFLICT (symbol, leg, time) 
                       DO UPDATE SET 
                         open = %s
                        ,high = %s
                        ,low = %s
                        ,close = %s
                        ,volume = %s
                    """
            # extras.execute_values(c, query, q)
            c.executemany(query, q)
            self.logger.info("insert_ohlcv() complete. {0}".format(record_count))
        except Exception as err:
            self.logger.error('error dayo. {0}'.format(err))
            if conn: conn.rollback()
        finally:
            if conn:
                conn.commit()
                conn.close


from lii3ra.mylogger import Logger
from lii3ra.dbaccess import DbAccess

s = Logger()
logger = s.myLogger()


class Ohlcv:
    def __init__(self, symbol, ashi, start_date, end_date):
        self.symbol = symbol
        self.ashi = ashi
        self.start_date = start_date
        self.end_date = end_date
        self.values = None
        self.get_ohlcv()

    def get_ohlcv(self):
        try:
            dba = DbAccess()
            df = dba.get_ohlcv(self.symbol, self.ashi, self.start_date, self.end_date)
            ohlcv_cnt = 0
            if not df.empty:
                self.values = df.fillna(method="ffill")
                ohlcv_cnt = len(self.values)
            else:
                self.values = None
            logger.info(f"ohlcv.get_ohlcv() [{self.symbol},{self.ashi},{self.start_date},{self.end_date}] count=[{ohlcv_cnt}]")
        except Exception as err:
            print(err)
        finally:
            if self.values.empty:
                raise Exception(f"No Data Exception:[{self.symbol}]")

    def get_headdate(self):
        if self.values.index.size != 0:
            return self.values.iloc[0]['time']
        else:
            return ""

    def get_taildate(self):
        if self.values.index.size != 0:
            return self.values.iloc[-1]['time']
        else:
            return ""

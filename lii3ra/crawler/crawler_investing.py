# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from datetime import datetime as dt
from datetime import timedelta
import investpy
import lii3ra.mylogger
from lii3ra.crawler.dbaccess import DbAccess


class InvestingCrawler:
    def __init__(self, logger=None):
        if logger is None:
            self.logger = lii3ra.mylogger.Logger().myLogger()
        else:
            self.logger = logger

    def download_historycal_data(self, symbol_list, start_date, end_date):
        from_date = dt.strptime(start_date, "%Y-%m-%d").strftime("%d/%m/%Y")
        to_date = dt.strptime(end_date, "%Y-%m-%d").strftime("%d/%m/%Y")
        for symbol_ary in symbol_list:
            data = None
            if symbol_ary[3] == "index":
                data = investpy.get_index_historical_data(index=symbol_ary[1]
                                                          , country=symbol_ary[2]
                                                          , from_date=from_date
                                                          , to_date=to_date)
            elif symbol_ary[3] == "etf":
                data = investpy.get_etf_historical_data(etf=symbol_ary[1]
                                                        , country=symbol_ary[2]
                                                        , from_date=from_date
                                                        , to_date=to_date)
            elif symbol_ary[3] == "stock":
                data = investpy.get_stock_historical_data(stock=symbol_ary[1]
                                                          , country=symbol_ary[2]
                                                          , from_date=from_date
                                                          , to_date=to_date)
            idx = data.index.size
            max_date = ''
            min_date = ''
            quotes = list()
            for i in range(idx):
                business_date = (data.index[i]).strftime("%Y-%m-%d")
                if symbol_ary[3] == "etf":
                    volume = 0
                else:
                    volume = int((data['Volume'][i]).astype('int64'))
                open_price = data['Open'][i]
                high_price = data['High'][i]
                low_price = data['Low'][i]
                close_price = data['Close'][i]
                quotes.append((symbol_ary[0], "1d", business_date, open_price, high_price, low_price, close_price, volume))
                if max_date == '':
                    max_date = business_date
                elif business_date > max_date:
                    max_date = business_date
                if min_date == '':
                    min_date = business_date
                elif business_date < min_date:
                    min_date = business_date
            dba = DbAccess()
            dba.insert_ohlcv(quotes)
            self.logger.info("downloaded:[%s][%s-%s] [%s-%s]" % (symbol_ary[0]
                                                                 , start_date
                                                                 , end_date
                                                                 , min_date
                                                                 , max_date))


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('--symbol', type=str, help='Absolute/relative path to input file')
    argparser.add_argument('--start_date', type=str, help='Date of backtest start')
    argparser.add_argument('--end_date', type=str, help='Date of backtest end')
    args = argparser.parse_args()
    return args


def crawler(symbol_list, start_date, end_date):
    s = lii3ra.mylogger.Logger()
    logger = s.myLogger('test')
    logger.info('crawler_investing.crawler() start.')
    InvestingCrawler().download_historycal_data(symbol_list, start_date, end_date)
    logger.info('crawler_investing.crawler() end.')


symbol_list = [
    ["^N225", "Nikkei 225", "japan", "index"]
    , ["Topix", "TOPIX", "japan", "index"]
    , ["JPX400", "JPX-Nikkei 400", "japan", "index"]
    , ["Mothers", "Topix Mother Market", "japan", "index"]
    , ["DJI", "Dow 30", "united states", "index"]
    , ["TREIT", "Topix REIT Market", "japan", "index"]
    , ["1321.T", "Nomura Nikkei 225 Listed", "japan", "etf"]
    , ["1570.T", "NEXT FUNDS Nikkei 225 Leveraged", "japan", "etf"]
    , ["1357.T", "NEXT FUNDS Nikkei 225 Double Inverse", "japan", "etf"]
    , ["1568.T", "Simplex TOPIX Bull 2x", "japan", "etf"]
    , ["1356.T", "Simplex TOPIX Bear -2x", "japan", "etf"]
    , ["1591.T", "NEXT FUNDS JPX-Nikkei 400", "japan", "etf"]
    , ["2516.T", "TSE Mothers", "japan", "etf"]
    , ["4755.T", "4755", "japan", "stock"]
    , ["8766.T", "8766", "japan", "stock"]
]


if __name__ == '__main__':
    args = get_option()
    if args.start_date is None:
        start_date = '2001-01-01'
    else:
        start_date = args.start_date
    if args.end_date is None:
        end_date = (dt.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        end_date = args.end_date
    crawler(symbol_list, start_date, end_date)


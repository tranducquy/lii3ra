# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd
import numpy as np
import threading
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
                quotes.append(
                    (symbol_ary[0], "1d", business_date, open_price, high_price, low_price, close_price, volume))
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
    argparser.add_argument('--start_date', type=str, help='Date of backtest start')
    argparser.add_argument('--end_date', type=str, help='Date of backtest end')
    args = argparser.parse_args()
    return args


def crawler_country(country_list, start_date, end_date):
    s = lii3ra.mylogger.Logger()
    logger = s.myLogger('test')
    logger.info('crawler_investing.crawler_country() start.')
    thread_pools = []
    # STOCKS
    cls = "stock"
    df = pd.read_csv("./lii3ra/symbol/stocks.csv")
    thread_pool = stocks_etfs(country_list, start_date, end_date, cls, df)
    # ETF
    cls = "etf"
    df = pd.read_csv("./lii3ra/symbol/etfs.csv")
    thread_pool2 = stocks_etfs(country_list, start_date, end_date, cls, df)
    thread_pool.extend(thread_pool2)
    thread_pool_cnt = len(thread_pool)
    split_num = (thread_pool_cnt / 8) + 1
    thread_pools = list(np.array_split(thread_pool, split_num))
    thread_join_cnt = 0
    for p in thread_pools:
        for t in p:
            t.start()
        for t in p:
            t.join()
            thread_join_cnt += 1
            logger.info("*** thread join[%d]/[%d] ***" % (thread_join_cnt, thread_pool_cnt))
    logger.info('crawler_investing.crawler_country() end.')


def stocks_etfs(country_list, start_date, end_date, cls, df):
    for c in country_list:
        country = c[0]
        suffix = c[1]
        stocks_df = df[df["country"] == country]
        symbol_list = []
        for row in stocks_df.itertuples():
            investing_symbol = row.symbol
            lii3ra_symbol = investing_symbol + suffix
            if cls == "stock":
                symbol_list.append([lii3ra_symbol, investing_symbol, country, cls])
            elif cls == "etf":
                symbol_list.append([lii3ra_symbol, row.name, country, cls])
        symbol_lists = np.array_split(symbol_list, 8)
        thread_pool = list()
        for symbol_list in symbol_lists:
            thread_pool.append(threading.Thread(target=InvestingCrawler().download_historycal_data, args=(symbol_list
                                                                                                          , start_date
                                                                                                          , end_date
                                                                                                          )))
        return thread_pool


country_list = [
    # ["japan", ".T"]
    ["united states", ""]
    , ["hong kong", ".HK"]
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
    crawler_country(country_list, start_date, end_date)

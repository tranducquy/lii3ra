# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from datetime import datetime as dt
from datetime import timedelta
import yfinance as yf
import lii3ra.mylogger
from lii3ra.crawler.dbaccess import DbAccess


class YfinanceCrawler:
    def __init__(self, logger=None):
        if logger is None:
            self.logger = lii3ra.mylogger.Logger().myLogger()
        else:
            self.logger = logger
        self.symbols = None
        self.start_date = None

    def download(self, symbols, start_date, end_date):
        self.symbols = symbols
        self.start_date = start_date
        self.end_date = end_date
        for symbol in symbols:
            data = yf.download(symbol, start=start_date, end=end_date)
            idx = data.index.size
            max_date = ''
            min_date = ''
            quotes = list()
            for i in range(idx):
                business_date = (data.index[i]).strftime("%Y-%m-%d")
                volume = int((data['Volume'][i]).astype('int64'))
                open_price = data['Open'][i]
                high_price = data['High'][i]
                low_price = data['Low'][i]
                close_price = data['Close'][i]
                quotes.append((symbol, "1d", business_date, open_price, high_price, low_price, close_price, volume))
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
            self.logger.info("downloaded:[%s][%s-%s] [%s-%s]" % (symbol, start_date, end_date, min_date, max_date))


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('--symbol', type=str, help='Absolute/relative path to input file')
    argparser.add_argument('--start_date', type=str, help='Date of backtest start')
    argparser.add_argument('--end_date', type=str, help='Date of backtest end')
    args = argparser.parse_args()
    return args


def crawler(symbols, start_date, end_date):
    s = lii3ra.mylogger.Logger()
    logger = s.myLogger('test')
    logger.info('crawler_yfinance.crawler() start.')
    YfinanceCrawler().download(symbols, start_date, end_date)
    logger.info('crawler_yfinance.crawler() end.')


# symbol
from lii3ra.symbol.yuusha_volume1b import Symbol
symbol_list = Symbol.symbols
temp_list = [
    "9107.T"
    , "^N225"
]
symbol_list.extend(temp_list)


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
    if args.symbol is None:
        symbols = symbol_list
    else:
        s = args.symbol
        symbols = s.split(',')
    crawler(symbols, start_date, end_date)

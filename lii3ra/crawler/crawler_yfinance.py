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

    def download(self, symbols, start_date, end_date):
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


default_symbols = [
    "1321.T"
    , "1356.T"
    , "1357.T"
    , "1568.T"
    , "1570.T"
    , "1571.T"
    , "3038.T"
    , "3288.T"
    , "4043.T"
    , "6141.T"
    , "6753.T"
    , "7717.T"
    , "7974.T"
    , "9104.T"
    , "9107.T"
    , "9424.T"
    , "5706.T"
    , "9616.T"
    , "4523.T"
    , "3088.T"
    , "2412.T"
    , "2427.T"
    , "9983.T"
    , "8876.T"
    , "6047.T"
    , "1568.T"
    , "6619.T"
    , "6762.T"
    , "4911.T"
    , "8267.T"
    , "4967.T"
    , "6141.T"
    , "8306.T"
    , "5411.T"
    , "6473.T"
    , "5713.T"
    , "6479.T"
    , "2503.T"
    , "1802.T"
    , "3141.T"
    , "9007.T"
    , "1570.T"
    , "9104.T"
    , "9107.T"
    , "^N225"
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
    if args.symbol is None:
        symbols = default_symbols
    else:
        s = args.symbol
        symbols = s.split(',')
    crawler(symbols, start_date, end_date)

# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime, timedelta
from argparse import ArgumentParser
from pytz import timezone
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import iso8601
import pytz
import lii3ra.mylogger
from lii3ra.crawler.oanda import OandaSymbol, OandaLeg
from lii3ra.crawler.oanda_account import OandaAccount
from lii3ra.crawler.dbaccess import DbAccess


class Crawler:
    def __init__(self, logger=None):
        if logger is None:
            self.logger = lii3ra.mylogger.Logger().myLogger()
        else:
            self.logger = logger

    def oanda_historical_download(self, symbol, leg, f, t):
        i = OandaSymbol.get_symbol(symbol)
        g = OandaLeg.get_leg(leg)
        api = API(access_token=OandaAccount.ACCESS_TOKEN)
        params = {
            "granularity": g,
            "from": f,
            "to": t
        }
        r = instruments.InstrumentsCandles(instrument=i, params=params)
        api.request(r)
        data = []
        for raw in r.response['candles']:
            raw_timestamp = iso8601.parse_date(raw['time'])
            tokyo_tz = pytz.timezone('Asia/Tokyo')
            # d = datetime.fromtimestamp(raw_timestamp.timestamp(), tokyo_tz).strftime('%Y-%m-%d-%H:%M:%S')
            d = datetime.fromtimestamp(raw_timestamp.timestamp(), tokyo_tz).isoformat()
            data.append([
                symbol
                , leg
                , d
                , raw['mid']['o']
                , raw['mid']['h']
                , raw['mid']['l']
                , raw['mid']['c']
                , raw['volume']
            ])
        return data

    def oanda_streaming_download(self, symbol, leg, c):
        i = OandaSymbol().get_symbol(symbol)
        g = OandaLeg().get_leg(leg)
        api = API(access_token=OandaAccount.ACCESS_TOKEN)
        params = {
            "granularity": g,
            "count": c
        }
        r = instruments.InstrumentsCandles(instrument=i, params=params)
        api.request(r)
        data = []
        for raw in r.response['candles']:
            raw_timestamp = iso8601.parse_date(raw['time'])
            tokyo_tz = pytz.timezone('Asia/Tokyo')
            d = datetime.fromtimestamp(raw_timestamp.timestamp(), tokyo_tz).isoformat()
            data.append([
                symbol
                , leg
                , d
                , raw['mid']['o']
                , raw['mid']['h']
                , raw['mid']['l']
                , raw['mid']['c']
                , raw['volume']
            ])
        return data

    def create_datelist(self, start_date, end_date):
        start_datetime = iso8601.parse_date(start_date + 'T00:00:00.000000+00:00')
        end_datetime = iso8601.parse_date(end_date + 'T23:59:59.999999+00:00')
        n = datetime.now(timezone('UTC'))
        datelist = []
        while start_datetime <= end_datetime:
            f = start_datetime.strftime('%Y-%m-%d') + 'T00:00:00.000000+00:00'
            t = start_datetime.strftime('%Y-%m-%d') + 'T23:59:59.999999+00:00'
            if t >= n.isoformat():
                t = n.isoformat()
                datelist.append([f, t])
                break
            datelist.append([f, t])
            start_datetime = start_datetime + timedelta(days=1)
        return datelist

    def crawl_daily(self, symbol, leg, start_date, end_date):
        dba = DbAccess()
        datelist = self.create_datelist(start_date, end_date)
        for d in datelist:
            q = self.oanda_historical_download(symbol, leg, d[0], d[1])
            dba.insert_ohlcv(q)
            self.logger.info("download {s},{leg},{start},{end}".format(s=symbol, leg=leg, start=d[0], end=d[1]))


def crawl_daily_all_leg(symbol, start_date, end_date):
    s = lii3ra.mylogger.Logger()
    logger = s.myLogger('test')
    logger.info('crawl_daily_all_leg().')
    crawler = Crawler()
    # シンボルのカンマ区切り対応
    symbols = [x.strip() for x in symbol.split(',')]
    for s in symbols:
        # 1秒足
        # leg = '1s'
        # crawler.crawl_daily(s, leg, start_date, end_date)
        # 5秒足
        # leg = '5s'
        # crawler.crawl_daily(s, leg, start_date, end_date)
        # 15秒足
        # leg = '15s'
        # crawler.crawl_daily(s, leg, start_date, end_date)
        # 30秒足
        # leg = '30s'
        # crawler.crawl_daily(s, leg, start_date, end_date)
        # 1分足
        leg = '1m'
        crawler.crawl_daily(s, leg, start_date, end_date)
        # 5分足
        leg = '5m'
        crawler.crawl_daily(s, leg, start_date, end_date)
        # 15分足
        leg = '15m'
        crawler.crawl_daily(s, leg, start_date, end_date)
        # 30分足
        leg = '30m'
        crawler.crawl_daily(s, leg, start_date, end_date)
        # 1時間足
        leg = '1h'
        crawler.crawl_daily(s, leg, start_date, end_date)
        # 4時間足
        leg = '4h'
        crawler.crawl_daily(s, leg, start_date, end_date)
        # 6時間足
        leg = '6h'
        crawler.crawl_daily(s, leg, start_date, end_date)
        # 8時間足
        leg = '8h'
        crawler.crawl_daily(s, leg, start_date, end_date)
        # 12時間足
        leg = '12h'
        crawler.crawl_daily(s, leg, start_date, end_date)
        # 1日足
        leg = '1d'
        crawler.crawl_daily(s, leg, start_date, end_date)


def streaming():
    pass


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('--symbol', type=str, help='symbol')
    argparser.add_argument('--start_date', type=str, help='Date of crawl start')
    argparser.add_argument('--end_date', type=str, help='Date of crawl end')
    argparser.add_argument('--daemon', action='store_true', help='daemonize!')
    args = argparser.parse_args()
    return args


def daemonize():
    def fork():
        if os.fork():
            sys.exit()

    def throw_away_io():
        stdin = open(os.devnull, 'rb')
        stdout = open(os.devnull, 'ab+')
        stderr = open(os.devnull, 'ab+', 0)
        for (null_io, std_io) in zip((stdin, stdout, stderr), (sys.stdin, sys.stdout, sys.stderr)):
            os.dup2(null_io.fileno(), std_io.fileno())

    fork()
    os.setsid()
    fork()
    throw_away_io()


if __name__ == '__main__':
    args = get_option()
    if args.start_date is None:
        start_date = (datetime.now() + timedelta(days=-3)).strftime('%Y-%m-%d')
    else:
        start_date = args.start_date
    if args.end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    else:
        end_date = args.end_date
    if args.symbol is None:
        symbol = 'USDJPY,EURJPY,GBPJPY,EURUSD,GBPUSD'
    else:
        symbol = args.symbol
    if args.daemon:
        daemonize()
        streaming()
    else:
        crawl_daily_all_leg(symbol, start_date, end_date)


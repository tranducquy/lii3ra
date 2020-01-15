# -*- coding: utf-8 -*-

from datetime import timedelta
import pandas as pd
from argparse import ArgumentParser
from lii3ra.mylogger import Logger
from lii3ra.crawler.dbaccess import DbAccess

s = Logger()
logger = s.myLogger('test')


def insert_investing_csv(symbol, csv_file, ashi):
    logger.info(f"read_csv() start. {symbol},{csv_file}")
    dba = DbAccess()
    historycal_data = read_csv(symbol, csv_file, ashi)
    dba.insert_ohlcv(historycal_data)
    logger.info("read_excel_all_sheet() end.")


def read_csv(symbol, csv_file, ashi):
    logger.info(f"read_csv() start. {symbol},{csv_file},{ashi}")
    df = pd.read_csv(csv_file)
    record_count = 0
    start_time = ""
    end_time = ""
    data = []
    for idx in range(len(df)):
        candle_time = pd.to_datetime(df['Date'][idx]).strftime("%Y-%m-%d")
        if type(df['Open'][idx]) is str:
            open_price = pd.to_numeric(df['Open'][idx].replace(',', ''))
        else:
            open_price = pd.to_numeric(df['Open'][idx])
        if type(df['High'][idx]) is str:
            high_price = pd.to_numeric(df['High'][idx].replace(',', ''))
        else:
            high_price = pd.to_numeric(df['High'][idx])
        if type(df['Low'][idx]) is str:
            low_price = pd.to_numeric(df['Low'][idx].replace(',', ''))
        else:
            low_price = pd.to_numeric(df['Low'][idx])
        if type(df['Low'][idx]) is str:
            close_price = pd.to_numeric(df['Price'][idx].replace(',', ''))
        else:
            close_price = pd.to_numeric(df['Price'][idx])
        temp = ''
        if type(df['Vol.'][idx]) is str:
            vol = df['Vol.'][idx]
            temp = vol.replace(',', '')
        if 'K' in temp:
            temp = temp.replace('K', '').replace('M', '').replace('B', '').replace('-', '')
            temp_volume = pd.to_numeric(temp) * 1000
        elif 'M' in temp:
            temp = temp.replace('K', '').replace('M', '').replace('B', '').replace('-', '')
            temp_volume = pd.to_numeric(temp) * 1000000
        elif 'B' in temp:
            temp = temp.replace('K', '').replace('M', '').replace('B', '').replace('-', '')
            temp_volume = pd.to_numeric(temp) * 1000000000
        else:
            temp_volume = None
        volume = pd.to_numeric(temp_volume)
        data.append([
            symbol
            , ashi
            , candle_time
            , open_price
            , high_price
            , low_price
            , close_price
            , volume
        ])
        record_count += 1
        if idx == 0:
            start_time = candle_time
        end_time = candle_time
    logger.info(f"read_csv() finish. {symbol},{ashi},{record_count},{start_time},{end_time}")
    return data


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('--symbol', type=str, help='symbol')
    argparser.add_argument('--file', type=str, help='excel file')
    args = argparser.parse_args()
    return args


if __name__ == '__main__':
    args = get_option()
    if args.symbol is None:
        symbol = 'Topix'
    else:
        symbol = args.symbol
    if args.file is None:
        csv_file = ""
    else:
        csv_file = args.file
    try:
        insert_investing_csv(symbol, csv_file, "1d")
    except Exception as e:
        logger.error(e)


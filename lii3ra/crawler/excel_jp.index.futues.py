# -*- coding: utf-8 -*-

from datetime import timedelta
import pandas as pd
from argparse import ArgumentParser
from lii3ra.mylogger import Logger
from lii3ra.crawler.dbaccess import DbAccess

s = Logger()
logger = s.myLogger('test')


def read_all_sheet(symbol, excel_file):
    logger.info(f"read_all_sheet() start. {symbol},{excel_file}")
    dba = DbAccess()
    n225_historycal_data = read_sheet(symbol, excel_file, 0, "1m")
    dba.insert_ohlcv(n225_historycal_data)
    dba = DbAccess()
    n225_historycal_data = read_sheet(symbol, excel_file, 1, "3m")
    dba.insert_ohlcv(n225_historycal_data)
    dba = DbAccess()
    n225_historycal_data = read_sheet(symbol, excel_file, 2, "5m")
    dba.insert_ohlcv(n225_historycal_data)
    dba = DbAccess()
    n225_historycal_data = read_sheet(symbol, excel_file, 3, "10m")
    dba.insert_ohlcv(n225_historycal_data)
    dba = DbAccess()
    n225_historycal_data = read_sheet(symbol, excel_file, 4, "15m")
    dba.insert_ohlcv(n225_historycal_data)
    dba = DbAccess()
    n225_historycal_data = read_sheet(symbol, excel_file, 5, "20m")
    dba.insert_ohlcv(n225_historycal_data)
    dba = DbAccess()
    n225_historycal_data = read_sheet(symbol, excel_file, 6, "30m")
    dba.insert_ohlcv(n225_historycal_data)
    dba = DbAccess()
    n225_historycal_data = read_sheet(symbol, excel_file, 7, "60m")
    dba.insert_ohlcv(n225_historycal_data)
    dba = DbAccess()
    n225_historycal_data = read_sheet(symbol, excel_file, 8, "1d", daily=True)
    dba.insert_ohlcv(n225_historycal_data)
    dba = DbAccess()
    n225_historycal_data = read_sheet(symbol, excel_file, 9, "1d_n", daily=True)
    dba.insert_ohlcv(n225_historycal_data)
    dba = DbAccess()
    n225_historycal_data = read_sheet(symbol, excel_file, 10, "1d_a", daily=True)
    dba.insert_ohlcv(n225_historycal_data)
    dba = DbAccess()
    n225_historycal_data = read_sheet(symbol, excel_file, 10, "1d_t", daily=True)
    dba.insert_ohlcv(n225_historycal_data)
    logger.info("read_excel_all_sheet() end.")


def read_sheet(symbol, excel_file, sheet, ashi, daily=False):
    logger.info(f"read_sheet() start. {symbol},{excel_file},{sheet},{ashi}")
    df = pd.read_excel(excel_file, sheet_name=sheet)
    record_count = 0
    start_time = ""
    end_time = ""
    data = []
    for idx in range(len(df)):
        if daily:
            candle_time = (df['日付'][idx]).strftime("%Y-%m-%d")
        else:
            temp_time = (df['時間'][idx]).strftime("%H:%M:%S")
            if "16:00:00" <= temp_time <= "23:59:59":  # 16:00:00-23:59:59
                temp_date = (df['日付'][idx] - timedelta(days=1)).strftime("%Y-%m-%d ")
                candle_time = temp_date + temp_time
            else:
                candle_time = (df['日付'][idx]).strftime("%Y-%m-%d ") + (df['時間'][idx]).strftime("%H:%M:%S")
        open_price = float(df['始値'][idx])
        high_price = float(df['高値'][idx])
        low_price = float(df['安値'][idx])
        close_price = float(df['終値'][idx])
        volume = float(df['出来高'][idx])
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
    logger.info(f"read_sheet() finish. {symbol},{ashi},{record_count},{start_time},{end_time}")
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
        symbol = 'N225minif'
    else:
        symbol = args.symbol
    if args.file is None:
        excel_file = ""
    else:
        excel_file = args.file
    try:
        read_all_sheet(symbol, excel_file)
    except Exception as e:
        logger.error(e)

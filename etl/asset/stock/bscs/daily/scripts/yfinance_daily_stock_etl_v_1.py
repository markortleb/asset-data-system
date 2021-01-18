from pymongo import MongoClient
import yfinance as yf #pip install yfinance
import os
from datetime import datetime, timedelta
import glob
import shutil
import time
import csv
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        '--ticker-symbol',
        dest='ticker_symbol',
        required=True,
        help='Ticker Symbol'
    )
    parser.add_argument(
        '-t',
        '--target-table',
        dest='target_table',
        required=True,
        help='Target Table'
    )
    parser.add_argument(
        '-d',
        '--target-database',
        dest='target_database',
        required=True,
        help='Target Database'
    )

    return parser.parse_known_args()


ARGS, UNKNOWN = parse_args()


def main():
    args = ARGS

    ticker_symbol = args.ticker_symbol
    target_table = args.target_table
    target_database = args.target_database

    start_date = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')

    mongo_client = MongoClient('localhost', 27017)
    asset_data_lake = mongo_client[target_database]
    target_table = asset_data_lake[target_table]
    ticker_df = yf.download(ticker_symbol, start=start_date)
    data = ticker_df.to_dict(orient='records')
    target_table.insert_many(data)



main()
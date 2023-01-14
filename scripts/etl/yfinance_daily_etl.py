from pymongo import MongoClient
import yfinance as yf #pip install yfinance
import os
from datetime import datetime, timedelta
import pytz
import glob
import shutil
import time
import csv
import argparse
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        '--ticker-symbol',
        dest='ticker_symbol',
        required=True,
        help='Ticker Symbol'
    )

    return parser.parse_known_args()


ARGS, UNKNOWN = parse_args()


def add_audit_columns(ticker_df, audit_load_epoch):
    ticker_df['audit_load_epoch'] = audit_load_epoch
    return ticker_df


def yfinance_to_mongo_rename(ticker_df):
    ticker_df = ticker_df.rename(
        columns={
            'Open': 'open',
            'Close': 'close',
            'High': 'high',
            'Low': 'low',
            'Adj Close': 'adj_close',
            'Volume': 'volume'
        }
    )
    ticker_df.index.names = ['date']
    return ticker_df


def convert_df_to_dict_with_index(df):
    index_name = df.index.names[0]
    df[index_name] = df.index
    df[index_name] = df[index_name].apply(lambda x: x.strftime('%Y-%m-%d'))
    df_dict = df.to_dict(orient='records')
    return df_dict


def get_yfinance_daily_df(ticker_symbol, start_date):
    audit_load_epoch = int(datetime.now().timestamp())
    ticker_df = yf.download(ticker_symbol, start=start_date)
    ticker_df = yfinance_to_mongo_rename(ticker_df)
    ticker_df = add_audit_columns(ticker_df, audit_load_epoch)
    return ticker_df  


def date_to_string(val):
    out_val = ''
    if type(val) == 'pandas._libs.tslibs.timestamps.Timestamp':
        out_val = val.strftime('%Y-%m-%d')
    elif type(val) == 'str':
        out_val = val

    return val


def merge_daily_df(new_df, old_df):
    """Merge YFinance Daily Dfs

    Args:
        new_df (pandas dataframe): DF containing YFinance Ticker Info, new read
        old_df (pandas dataframe): DF containing Stored MongoDB Ticker Info, old read

    Returns:
        pandas dataframe: A DF containing data from new_df, merged with old_df
    """
    # Delete '_id' column that is added from mongo
    del old_df['_id']

    # Set new_df index to be the 'date' column and delete index
    index_name = new_df.index.names[0]
    new_df[index_name] = new_df.index
    # new_df[index_name] = new_df[index_name].apply(lambda x: x.strftime('%Y-%m-%d'))
    new_df.reset_index(drop=True, inplace=True)

    # Append old_df to new_df and dedup
    new_df = new_df.append(old_df)
    new_df['date'] = new_df['date'].apply(lambda x: date_to_string(x))
    new_df = new_df.sort_values(by='audit_load_epoch', ascending=False)
    new_df = new_df.drop_duplicates(subset='date', keep='first')
    new_df = new_df.sort_values(by='date')
    
    # Set the new_df index back to 'date' and delete 'date' column
    new_df.index.name = 'date'
    new_df.index = new_df['date']
    del new_df['date']

    return new_df


def main():
    args = ARGS
    ticker_symbol = args.ticker_symbol
    target_table_name = f'{ticker_symbol.lower()}_yfinance_daily_extracts'
    target_database_name = 'asset_database'
    start_date = '2018-11-20'
    current_datetime_est = datetime.now(pytz.timezone('US/Eastern'))

    print('running')

    if current_datetime_est.weekday() not in [5, 6] or True:
        ticker_df = get_yfinance_daily_df(ticker_symbol, start_date)
        
        mongo_client = MongoClient('asset_data_system_db', 27017)
        target_database = mongo_client[target_database_name]
        target_table = target_database[target_table_name]

        if target_table.count_documents({}) > 0:
            target_table_cursor = target_table.find({})
            target_table_df = pd.DataFrame(list(target_table_cursor))
            out_df = merge_daily_df(ticker_df, target_table_df)
        else:
            out_df = ticker_df

        out_dict = convert_df_to_dict_with_index(out_df)

        target_table.drop()
        target_table.insert_many(out_dict)


main()

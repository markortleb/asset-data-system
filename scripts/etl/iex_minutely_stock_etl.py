from datetime import datetime, timedelta
from pymongo import MongoClient
import requests
import argparse
import json
import yaml
import os
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
    parser.add_argument(
        '-t',
        '--target-table-name',
        dest='target_table_name',
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
    parser.add_argument(
        '-r',
        '--repo-path',
        dest='repo_path',
        required=True,
        help='Repo Path'
    )
    parser.add_argument(
        '-m',
        '--test',
        dest='test',
        help='Test', 
        action='store_true'
    )

    return parser.parse_known_args()


ARGS, UNKNOWN = parse_args()


def download_historical_intraday(ticker_symbol, iex_token, test, date):
    date_string = date.strftime('%Y-%m-%d')
    date_string_no_dash = date.strftime('%Y%m%d')
    if test:
        base_url = 'sandbox.iexapis.com'
    else:
        base_url = 'cloud.iexapis.com'

    request_string = f'https://{base_url}/stable/stock/{ticker_symbol}/chart/date/{date_string_no_dash}?token={iex_token}'

    r = requests.get(request_string)
    json_list = json.loads(r.text)
    
    if json_list:
        intraday_df = pd.DataFrame.from_dict(json_list, orient='columns')

        # Set the new_df index back to 'date' and delete 'date' column
        intraday_df.index.name = 'date'
        intraday_df.index = intraday_df['date']
        del intraday_df['date']
    else:
        intraday_df = None
    
    return intraday_df


def download_current_intraday(ticker_symbol, iex_token, test, date):
    date_string = date.strftime('%Y-%m-%d')
    date_string_no_dash = date.strftime('%Y%m%d')
    if test:
        base_url = 'sandbox.iexapis.com'
    else:
        base_url = 'cloud.iexapis.com'

    request_string = f'https://{base_url}/stable/stock/{ticker_symbol}/intraday-prices?token={iex_token}'

    r = requests.get(request_string)
    json_list = json.loads(r.text)

    if json_list:
        intraday_df = pd.DataFrame.from_dict(json_list, orient='columns')

        # Set the new_df index back to 'date' and delete 'date' column
        intraday_df.index.name = 'date'
        intraday_df.index = intraday_df['date']
        del intraday_df['date']
    else:
        intraday_df = None
    
    return intraday_df


def get_intraday_df(ticker_symbol, iex_token, test, current_date, iter_date):
    if iter_date != current_date:
        intraday_df = download_historical_intraday(
            ticker_symbol, 
            iex_token, 
            test, 
            iter_date
        )
    else:
        intraday_df = download_current_intraday(
            ticker_symbol, 
            iex_token, 
            test, 
            iter_date
        )
    
    return intraday_df


def convert_df_to_dict_with_index(df):
    index_name = df.index.names[0]
    df[index_name] = df.index
    df[index_name] = df[index_name].apply(lambda x: x)
    df_dict = df.to_dict(orient='records')
    return df_dict


def load_intraday_data(ticker_symbol, target_database, target_table_name, iex_token, test):
    mongo_client = MongoClient('localhost', 27017)
    asset_data_lake = mongo_client[target_database]
    target_table = asset_data_lake[target_table_name]

    current_date = datetime.now()
    last_30_days_date = (current_date - timedelta(days=30))
    iter_date = last_30_days_date

    audit_load_epoch = int(current_date.timestamp())
    
    while iter_date <= current_date:
        # This is Mountain Time, not UTC. Change later...
        iter_market_open = iter_date.replace(hour=7, minute=30, second=0, microsecond=0)
        iter_market_close = iter_date.replace(hour=14, minute=0, second=0, microsecond=0)
        iter_date_string = iter_date.strftime('%Y-%m-%d')
        if iter_date.weekday() not in [5, 6]:
            print(f'Loading Intraday {ticker_symbol} data for {iter_date_string}')

            target_table_partition_cursor = target_table.find(
                {
                    'date': {'$eq': iter_date_string}
                }
            )
            target_table_partition_df = pd.DataFrame(list(target_table_partition_cursor))

            # If there exists previously written partition, overwrite. If not, just write
            if target_table_partition_cursor.count() > 0:
                current_loaded_epoch = list(set(target_table_partition_df['audit_load_epoch'].to_list()))

                # Only load to previously written partitions IF the existing partition was written before end of (full) day
                if current_loaded_epoch[0] <= (iter_date + timedelta(days=1)).timestamp():
                    intraday_df = get_intraday_df(
                        ticker_symbol, 
                        iex_token, 
                        test,
                        current_date,
                        iter_date
                    )
                    if intraday_df is not None:
                        intraday_df['audit_load_epoch'] = audit_load_epoch
                        out_dict = convert_df_to_dict_with_index(intraday_df)

                        target_table.remove(
                            {
                                'date': {'$eq': iter_date_string}
                            }
                        )
                        target_table.insert_many(out_dict)
            else:
                intraday_df = get_intraday_df(
                    ticker_symbol, 
                    iex_token, 
                    test,
                    current_date,
                    iter_date
                )
                if intraday_df is not None:
                    intraday_df['audit_load_epoch'] = audit_load_epoch
                    out_dict = convert_df_to_dict_with_index(intraday_df)
                    target_table.insert_many(out_dict)
                else:
                    # Write a dummy holder document to table so we don't try loading this day again, hence saving API calls
                    dummy_dict = {
                        'error': 'HOLIDAY',
                        'date': iter_date_string,
                        'audit_load_epoch': audit_load_epoch + 100
                    }
                    target_table.insert_many([dummy_dict])


        iter_date = (iter_date + timedelta(days=1))


def main():
    args = ARGS
    ticker_symbol = args.ticker_symbol
    target_table_name = args.target_table_name
    target_database = args.target_database
    repo_path = os.path.expanduser(args.repo_path)
    test = args.test

    if test:
        # If test, use the API Sandbox Key
        iex_token = 'Tsk_9ee49fcf8c914e16b38c7ff7ed8a5f00'
    else:
        # If not test, use our Secret Key
        with open(f'{repo_path}/infrastructure/general_config.yml', 'r') as stream:
            iex_key_path = yaml.safe_load(stream)['iex_key_path']
        with open(os.path.expanduser(iex_key_path), 'r') as stream:
            iex_keys = yaml.safe_load(stream)['keys']
            iex_token = iex_keys['secret_key']

    load_intraday_data(ticker_symbol, target_database, target_table_name, iex_token, test)


main()

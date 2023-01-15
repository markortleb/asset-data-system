from datetime import datetime, timedelta
from pymongo import MongoClient
import pandas as pd


def get_mongo_collection(collection_name):
    database_name = 'asset_database'
    mongo_client = MongoClient('asset_data_system_db', 27017)
    database = mongo_client[database_name]
    collection = database[collection_name]
    return collection


def get_yahoo_daily_df(ticker_symbol):
    collection_name = f'{ticker_symbol.lower()}_yfinance_daily_extracts'
    collection = get_mongo_collection(collection_name)

    lower_limit_date = (datetime.now() - timedelta(days=150))

    collection_cursor = collection.find(
        {
            'date': {
                '$gte': lower_limit_date.strftime('%Y-%m-%d')
            }
        }
    )
    ticker_df = pd.DataFrame(list(collection_cursor))
    ticker_df = ticker_df.rename(
        columns={
            'open': 'Open',
            'close': 'Close',
            'high': 'High',
            'low': 'Low',
            'volume': 'Volume',
            'date': 'Date'
        }
    )

    ticker_df['Date'] = ticker_df['Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

    ticker_df.index = ticker_df['Date']
    ticker_df.index.name = 'Date'
    del ticker_df['Date']

    return ticker_df

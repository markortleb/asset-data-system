from pymongo import MongoClient


def main():
    mongo_client = MongoClient('localhost', 27017)
    asset_data_lake = mongo_client['asset_data_lake']
    print(asset_data_lake)


main()

import requests
import datetime
import pandas as pd
import json
pd.set_option('display.max_rows', 500)
from sqlalchemy import create_engine



def get_historical_rates(user, password, host, port, db, table_name, execution_date):
    print("Loading historical data")
    print(execution_date)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    with engine.connect() as conn:

        params = {'base': 'BTC', "symbols": ["USD"]}
        url = f'https://api.exchangerate.host/{execution_date}'
        response = requests.get(url, params)
        data = response.json()
        data_dict = {execution_date: data['rates']}

        df = pd.DataFrame.from_dict(data_dict, orient='index').round(2)
        df = df.reset_index()

        df.columns = ["date", "exchange_rate"]; df['pair'] = "BTC/USD"
        df.date = pd.to_datetime(df.date)
        print(df)

        if execution_date == "2020-01-01":
            print("Table Doesn't Exist, creating ...")
            df.head(n=0).to_sql(name=table_name, con=conn, index=False, if_exists='replace')

        df.to_sql(name=table_name, con=conn, index=False, if_exists='append')




def get_latest_rates(user, password, host, port, db, table_name):
    print("Loading latest data")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    with engine.connect() as conn:

        params = {'base': 'BTC', "symbols": ["USD"]}
        url = 'https://api.exchangerate.host/latest'
        response = requests.get(url, params)
        data = response.json()

        data_dict = {datetime.datetime.now(): data['rates']}

        df = pd.DataFrame.from_dict(data_dict, orient='index').round(2)
        df = df.reset_index()

        df.columns = ["date", "exchange_rate"]; df['pair'] = "BTC/USD"
        df.date = pd.to_datetime(df.date)
        print(df)

        df.to_sql(name=table_name, con=conn, index=False, if_exists='append')










if __name__ == "__main__":
    # Making a request
    params = {'base': 'BTC', "symbols": ["USD"]}
    url = 'https://api.exchangerate.host/latest'
    response = requests.get(url, params)
    data = response.json()

    data_dict = {datetime.datetime.now(): data['rates']}
    print(data_dict)










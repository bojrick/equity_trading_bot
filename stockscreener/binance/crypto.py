import pandas as pd
from pandas.core.base import DataError
from binance.client import Client
import datetime
import config
import psycopg2

def binanceBarExtractor(symbol,table_name,start_date,end_date):
    print('working...')
    # filename = '{}_MinuteBars.csv'.format(symbol)

    klines = bclient.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, start_date.strftime("%d %b %Y %H:%M:%S"), end_date.strftime("%d %b %Y %H:%M:%S"), 1000)
    df = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    print("Shape of the dataframe:",df.shape)
    #data.set_index('timestamp', inplace=True)
    #data.to_csv(filename)
    
    if len(df) > 0:
        df_columns = list(df)
        # create (col1,col2,...)
        columns = ",".join(df_columns)
        # table = "CREATE TABLE IF NOT EXISTS snapshot LIKE source_data;"
        # create VALUES('%s', '%s",...) one '%s' per column
        values = "VALUES({})".format(",".join(["%s" for _ in df_columns])) 

        #create INSERT INTO table (columns) VALUES('%s',...)
        insert_stmt = "INSERT INTO {} ({}) {}".format(table_name,columns,values)

        cur = conn.cursor()
        psycopg2.extras.execute_batch(cur, insert_stmt, df.values)
        conn.commit()
        #cur.close()


if __name__ == '__main__':
    # Obviously replace BTCUSDT with whichever symbol you want from binance
    # Wherever you've saved this code is the same directory you will find the resulting CSV file
    # Connect to your postgres DB
    CONNECTION = "postgres://baymax:carbonara@localhost:5432/crypto_klines"
    conn = psycopg2.connect("dbname=crypto_klines user=postgres")
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    bclient = Client(api_key=config.binance_api_key, api_secret=config.binance_api_secret)
    base = datetime.datetime.strptime('25 Dec 2020', '%d %b %Y')
    date_list = [base - datetime.timedelta(days=x) for x in range(3000)]
    date_list.reverse()
    for idx in date_list:
        print("start_date : {}, end_date: {}".format(date_list[0],date_list[1]))
        binanceBarExtractor('BTCUSDT',table_name='BTCUSDT',start_date=date_list[0],end_date=date_list[1])
    
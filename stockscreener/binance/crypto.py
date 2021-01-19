import pandas as pd
from pandas.core.base import DataError
from binance.client import Client
import datetime
import config
import psycopg2
import psycopg2.extras

def binanceBarExtractor(symbol,table_name,start_date,end_date):
    # print('working...')
    # filename = '{}_MinuteBars.csv'.format(symbol)

    klines = bclient.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, start_date.strftime("%d %b %Y %H:%M:%S"), end_date.strftime("%d %b %Y %H:%M:%S"), 1000)
    df = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    # df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    # print("Shape of the dataframe:",df.shape)
    # print(df.head())
    #data.set_index('timestamp', inplace=True)
    #data.to_csv(filename)
    
    if len(df) > 0:
        df_columns = list(df)
        # create (col1,col2,...)
        columns = ",".join(df_columns)
        # table = f"""CREATE TABLE {str(table_name)} (
        #     {df_columns[0]} bigint NOT NULL,
        #     {df_columns[1]} money NOT NULL,
        #     {df_columns[2]} money NOT NULL,
        #     {df_columns[3]} money NOT NULL,
        #     {df_columns[4]} money NOT NULL,
        #     {df_columns[5]} numeric NOT NULL,
        #     {df_columns[6]} bigint NOT NULL,
        #     {df_columns[7]} numeric NOT NULL,
        #     {df_columns[8]} numeric NOT NULL,
        #     {df_columns[9]} numeric NOT NULL,
        #     {df_columns[10]} numeric NOT NULL,
        #     {df_columns[11]} numeric NOT NULL);"""
        # print(table)
        # create VALUES('%s', '%s",...) one '%s' per column
        values = "VALUES({})".format(",".join(["%s" for _ in df_columns])) 
        #create INSERT INTO table (columns) VALUES('%s',...)
        insert_stmt = f"INSERT INTO {table_name}({columns}) {values}"
        cur = conn.cursor()
        psycopg2.extras.execute_batch(cur, insert_stmt,df.values)
        conn.commit()
        #cur.close()


if __name__ == '__main__':
    # Obviously replace BTCUSDT with whichever symbol you want from binance
    # Wherever you've saved this code is the same directory you will find the resulting CSV file
    # Connect to your postgres DB
    CONNECTION = "postgres://baymax:carbonara@localhost:5432/crypto_klines"
    conn = psycopg2.connect("dbname=crypto_klines user=postgres")
    print(conn)
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    
    bclient = Client(api_key=config.binance_api_key, api_secret=config.binance_api_secret)
    
    base = datetime.datetime.strptime('16 Jan 2021', '%d %b %Y')
    date_list = [base - datetime.timedelta(days=x) for x in range(2500)]
    date_list.reverse()
    for idx in range(len(date_list)-1):
        print("start_date : {}, end_date: {}".format(date_list[idx],date_list[idx+1]))
        binanceBarExtractor('BTCUSDT',table_name="btcusdt3k",start_date=date_list[idx],end_date=date_list[idx+1])
    
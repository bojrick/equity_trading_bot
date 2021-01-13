from config import PAPER_API_KEY, PAPER_SECRET_KEY
import alpaca_trade_api as tradeapi
import config
import pandas as pd
import psycopg2
import time

#Connect to your postgres DB
CONNECTION = "postgres://postgres:carbonara@localhost:5432/min_bars"

conn = psycopg2.connect("dbname=min_bars user=postgres")
print(conn)
cur = conn.cursor()
cur.execute("ROLLBACK")

NY = 'America/New_York'
api = tradeapi.REST(config.PAPER_API_KEY,config.PAPER_SECRET_KEY, base_url='https://paper-api.alpaca.markets')
# Minute data example

list_assets = pd.read_csv('list_assets.csv').sort_values(by='symbol')
list_assets['tradable'] = list_assets['tradable']
tradebles = list_assets[list_assets['tradable']==True]
tickers_list = tradebles['symbol'].str.replace('-','_')

def prep_sql_queries(tick,start,end):
    
    sql_string = 'INSERT INTO {} '.format(tick) 
    columns = ['time','open','high','low','close','volume']
    sql_string += "(" + ', '.join(columns) + ")\nVALUES "
    record_list = api.get_barset(tick, 'minute', start=start, end=end)[tick]._raw
        # enumerate over the record
    
    for record_dict in record_list:
        values = []
        for val in record_dict.values():
            values.append(str(val))
        
        sql_string+='({}),\n'.format(', '.join(values))
    
    return sql_string[:-2]+';'

start=pd.Timestamp('2020-12-20 4:00', tz=NY).isoformat()
end=pd.Timestamp('2020-12-27 18:00', tz=NY).isoformat()
# print(prep_sql_queries('AAPL',start,end))
for tick in tickers_list:
    try:
        print('Saving data of {}'.format(tick))
        create_table_string = '''CREATE TABLE {} (
        time bigint,
        open numeric,
        high numeric,
        low numeric,
        close numeric,
        volume numeric);'''.format(tick)
        cur.execute(create_table_string)
        cur.execute('\d+')
        cur.execute(prep_sql_queries(tick,start,end))
        conn.commit()
        print('{} Table added to the database'.format(tick))
        # print('Sleeping for 100 seconds')
        # time.sleep(10)
    except (Exception, psycopg2.Error) as error :
        if(conn):
            print("Failed to insert record into table", error)

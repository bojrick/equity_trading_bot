import config
import websocket
import json
from datetime import datetime
import pandas as pd
import psycopg2
import models
from sqlalchemy.orm import Session
from database import SessionLocal, engine

# Connect to your postgres DB
# CONNECTION = "postgres://admin:carbonara@localhost:5432/sales"
# conn = psycopg2.connect("dbname=sales user=postgres")
# cur = conn.cursor()
# cur.execute("ROLLBACK")

models.Base.metadata.create_all(bind=engine)
daily_table = sqlalchemy.Table('daily_data', modeels.meta, autoload = True)
def recreate_database():
    models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(engine)

for user in json:
    query = daily_table.insert()
    query.values(**user)

    my_session = SessionLocal(engine)
    my_session.execute(query)
    my_session.close()

print(db.query(models.Book).first())
db.close()
# class StockRequest(BaseModel):
#     symbol: str

# def get_db():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()

# stmt = users.insert().\
#         values(name=bindparam('_name') + " .. name")
# conn.execute(stmt, [
#        {'id':4, '_name':'name1'},
#        {'id':5, '_name':'name2'},
#        {'id':6, '_name':'name3'},
#     ])


#  on_open(ws):
#     print("opened")
#     auth_data = {
#         "action": "authenticate",
#         "data": {"key_id": config.MARKET_API, "secret_key": config.MARKET_SECRET_KEY}
#     }
#     ws.send(json.dumps(auth_data))
#     listen_message = {"action": "listen", "data": {"streams": ["AM.*"]}}
#     ws.send(json.dumps(listen_message))

# #savee the lisenting data in database  
# def on_message(ws, json_message):
#     print("____received a message______")
#     dict_message = json.loads(json_message)
#     am_bar = dict_message['data']
#     print('op' in am_bar)
#     if 'op' in am_bar:
#         try:
#             postgres_insert_query = """ INSERT INTO am_data (beg_time,
#                                                      end_time,
#                                                      symbol,
#                                                      volume,
#                                                      acc_vol,
#                                                      off_open_price,
#                                                      vwap,
#                                                      open_price,
#                                                      high_price,
#                                                      low_price,
#                                                      close_price,
#                                                      avg_price) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
#             record_to_insert = (am_bar['s'],
#                                 am_bar['e'],
#                                 am_bar['T'],
#                                 am_bar['v'],
#                                 am_bar['av'],
#                                 am_bar['op'],
#                                 am_bar['vw'],
#                                 am_bar['o'],
#                                 am_bar['h'],
#                                 am_bar['l'],
#                                 am_bar['c'],
#                                 am_bar['a'])

#             print(record_to_insert)
#             cur.execute(postgres_insert_query, record_to_insert)
#             cur.commit()
            
#         except (Exception, psycopg2.Error) as error :
#             if(conn):
#                 print("Failed to insert record into data table", error)


# def on_pandas(ws, json_message):
#     print("____received a message______")
#     dict_message = json.loads(json_message)
#     am_bar = dict_message['data']
#     print(am_bar)
#     print(pd.DataFrame(am_bar).head(5))
    

# def on_close(ws):
#     cur.close()
#     print("closed connection")

# socket = "wss://data.alpaca.markets/stream"
# ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_pandas, on_close=on_close)
# ws.run_forever()

import config
import websocket
import json
from database import SessionLocal, engine
from models import dailyData
import datetime
from sqlalchemy.orm import Session
import models
from pydantic import BaseModel 

models.Base.metadata.create_all(bind=engine)

def on_open(ws):
    print("opened")
    auth_data = {
        "action": "authenticate",
        "data": {"key_id": config.MARKET_API, "secret_key": config.MARKET_SECRET_KEY}
    }

    ws.send(json.dumps(auth_data))

    listen_message = {"action": "listen", "data": {"streams": ["AM.SPY","AM.TSLA"]}}

    ws.send(json.dumps(listen_message))

response_id = 0
def on_message(ws, json_message):
    print("____received a message______")
    dict_message = json.loads(json_message)
    print('msg = ', dict_message)
    print('condn__', 'o' in dict_message['data'])
    print('\n')
    if 'o' in dict_message['data']:
        db = SessionLocal()
        dd = dailyData()
        response_id+=1
        print('id',response_id)
        dd.response_id = response_id
        bt = datetime.datetime.fromtimestamp(int(dict_message["data"]["s"])/1e3)
        et = datetime.datetime.fromtimestamp(int(dict_message["data"]["e"])/1e3)
        dd.beg_time = f"{bt:%Y-%m-%d %H:%M:%S}"
        dd.end_time = f"{et:%Y-%m-%d %H:%M:%S}"
        dd.symbol = dict_message["data"]["T"]
        dd.event = dict_message["data"]["ev"]
        dd.vol = dict_message["data"]["v"]
        dd.acc_vol = dict_message["data"]["av"]
        dd.off_open_price = dict_message["data"]["op"]
        dd.vwap = dict_message["data"]["vw"]
        dd.o = dict_message["data"]["o"]
        dd.high = dict_message["data"]["h"]
        dd.low = dict_message["data"]["l"]
        dd.close = dict_message["data"]["c"]
        dd.avg = dict_message["data"]["a"]
        db.add(dd)
        db.commit()

def on_close(ws):
    print("closed connection")

socket = "wss://data.alpaca.markets/stream"
ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()
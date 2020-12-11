import config
import websocket
import json
from database import SessionLocal, engine
from models import Stock, dailyData
import datetime


def on_open(ws):
    print("opened")
    auth_data = {
        "action": "authenticate",
        "data": {"key_id": config.MARKET_API, "secret_key": config.MARKET_SECRET_KEY}
    }

    ws.send(json.dumps(auth_data))

    listen_message = {"action": "listen", "data": {"streams": ["Q.SPY"]}}

    ws.send(json.dumps(listen_message))

db = SessionLocal()
def on_message(ws, message):
    print("received a message")
    message = json.loads(message)
    print('msg = ', message)
    #row = stock = db.query(Stock).filter(Stock.id == id).first()
    print('condn', 'p' in list(message['data'].keys()))
    if 'p' not in list(message['data'].keys()):
        print('iff')
        dd = dailyData()
        print('dd = ',dd)
        #ts = message["data"]["t"]
        
        #print('ts =',ts)
        #ts = datetime.utcfromtimestamp(int(ts)/1e9).strftime('%Y-%m-%d %H:%M:%S')
        #print('ts now=',ts)
        dd.id = "2020-12-10 18:59:57"#f"{ts:%Y-%m-%d %H:%M:%S}"
        dd.price = 8#message["data"]["p"]

        db.add(dd)
        db.commit()

def on_close(ws):
    print("closed connection")


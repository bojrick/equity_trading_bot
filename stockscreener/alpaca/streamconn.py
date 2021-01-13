from alpaca_trade_api import StreamConn
import alpaca_trade_api as tradeapi
from config import *
import threading

conn = tradeapi.stream2.StreamConn(PAPER_API_KEY, PAPER_SECRET_KEY, PAPER_BASE_URL,data_url=ws_url, data_stream='alpacadatav1')

@conn.on(r'^T.AAPL$')
async def trade_info(conn, channel, bar):
    print('bars', bar)
    print(bar._raw)

@conn.on(r'^T.AAPL$')
async def trade_info(conn, channel, bar):
    print('bars', bar)
    print(bar._raw)

@conn.on(r'^AM.AAPL$')
async def on_minute_bars(conn, channel, bar):
    print('bars', bar)

@conn.on(r'^trade_updates$')
async def on_trade_updates(conn, channel, trade):
    print('trade', trade)

def ws_start():
	conn.run(['account_updates', 'trade_updates'])

#start WebSocket in a thread
ws_thread = threading.Thread(target=ws_start, daemon=True)
ws_thread.start()

conn.run(['AM.AAPL'])

from configurations import BITFINEX_ENDPOINT

import time

import asyncio
import websockets

from websockets.legacy.client import connect as ws_connect

import json

async def hello(uri):
    request = json.dumps({
    "event": "subscribe",
    "channel": "book",
    "pair": "BTCUSD",
    "prec": "P0"
})

    async with ws_connect(uri) as websocket:
        while True:
            try:
                await websocket.send(request)
                msg = await websocket.recv()
                print(json.loads(msg))

            except websockets.ConnectionClosed as exception:
                print(exception)

            time.sleep(0.25)

            

         



asyncio.get_event_loop().run_until_complete(hello('wss://api-pub.bitfinex.com/ws/2'))

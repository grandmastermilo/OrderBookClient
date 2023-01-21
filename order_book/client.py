from configurations import BITFINEX_ENDPOINT

from order_book.orderbook import OrderBook
from order_book.handler import Handler

import json
import websockets
from websockets.legacy.client import connect as ws_connect

from multiprocessing import Queue
from threading import Thread



class BitfinexClient(Thread):

    def __init__(self):
        """
        Constructor for bitfinex client message handler
        """
        #TODO clean this
        super(BitfinexClient, self).__init__(name='demo', daemon=True)

        self.OB_request = json.dumps({
            "event": "subscribe",
            "channel": "book",
            "pair": "BTCUSD",
            "prec": "R0"
        })


        self.orderbook = OrderBook()
        self.handler = Handler(self.orderbook)

        self.queue = Queue()



    async def subscribe_OB(self):
        """
        Method for handling income message from the bitfinex websocket
        """

        try:
            self.ws = await ws_connect('wss://api-pub.bitfinex.com/ws/2')

            await self.ws.send(self.OB_request)

            while True:
                self.queue.put(json.loads(await self.ws.recv()))

        except websockets.ConnectionClosed as exception:
            #Handle time out, lost connecting recon
            pass



    def run(self) -> None:
        """
        Process incoming message FIFO
        """
        while True:
            msg = self.queue.get()
            self.handler.on_message(msg)





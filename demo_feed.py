from configurations import LOGGER, BITFINEX_ENDPOINT, MAX_RECONNECTION_ATTEMPTS, TIMEZONE

from multiprocessing import Queue
from threading import Thread
from multiprocessing import Process
import websockets
from datetime import datetime as dt
import json

import time

print(BITFINEX_ENDPOINT)

class Client(Process):

    def __init__(self):

        return

    def run(self):

        worker = DemoClient()
        worker.start()

        
        return


class DemoClient(Thread):

    def __init__(self):
        super(DemoClient, self).__init__(name=('BTC-USD', 'tBTCUSD'), daemon=True)

        self.exchange = 'bitfinex'
        self.queue = Queue(maxsize=0)

        self.request = json.dumps({
            "event": "subscribe",
            "channel": "book",
            "prec": "R0",
            "freq": "F0",
            "symbol": ('BTC-USD', 'tBTCUSD'),
            "len": "100"
        })
        self.request_unsubscribe = None
        self.trades_request = json.dumps({
            "event": "subscribe",
            "channel": "trades",
            "symbol": ('BTC-USD', 'tBTCUSD')
        })

        self.ws_endpoint = BITFINEX_ENDPOINT
        self.ws = None

        self.max_retries = 5
        self.retry_counter = 0


        self.sym = ('BTC-USD', 'tBTCUSD')
        return

    def run(self):

        while True:
            print(self.queue.get())
            msg = self.queue.get()
            print(msg)
            input()

        return 

    async def subscribe(self) -> None:
        """
        Subscribe to full order book.
        """
        try:
            self.ws = await websockets.connect(self.ws_endpoint)

            if self.request is not None:
                LOGGER.info('Requesting Book: {}'.format(self.request))
                await self.ws.send(self.request)
                LOGGER.info('BOOK %s: %s subscription request sent.' %
                            (self.exchange.upper(), self.sym))

            if self.trades_request is not None:
                LOGGER.info('Requesting Trades: {}'.format(self.trades_request))
                await self.ws.send(self.trades_request)
                LOGGER.info('TRADES %s: %s subscription request sent.' %
                            (self.exchange.upper(), self.sym))

            self.last_subscribe_time = dt.now(tz=TIMEZONE)

            # Add incoming messages to a queue, which is consumed and processed
            #  in the run() method.
            while True:
                self.queue.put(json.loads(await self.ws.recv()))

        except websockets.ConnectionClosed as exception:
            LOGGER.warn('%s: subscription exception %s' % (self.exchange, exception))
            self.retry_counter += 1
            elapsed = (dt.now(tz=TIMEZONE) - self.last_subscribe_time).seconds

            if elapsed < 10:
                sleep_time = max(10 - elapsed, 1)
                time.sleep(sleep_time)
                LOGGER.info('%s - %s is sleeping %i seconds...' %
                            (self.exchange, self.sym, sleep_time))

            if self.retry_counter < self.max_retries:
                LOGGER.info('%s: Retrying to connect... attempted #%i' %
                            (self.exchange, self.retry_counter))
                await self.subscribe()  # recursion
            else:
                LOGGER.warn('%s: %s Ran out of reconnection attempts. '
                            'Have already tried %i times.' %
                            (self.exchange, self.sym, self.retry_counter))
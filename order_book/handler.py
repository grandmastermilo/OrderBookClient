from order_book.orderbook import OrderBook
from order_book.side import Side
from order_book.order import Order

class Handler:

    def __init__(self, orderbook:OrderBook) -> None:
        """
        Handler constructor

        - used for processing messages for the orer



        EVENTS
            - info : inital message received estabilshing a connection
            - subscribe : confirmation of our subscriptions to the websocket

        STREAM
            - checksum : 'cs' token and checksum value 
            - snapshots : contain a list of orders
                    [
                        CHANNEL_ID,
                        [
                            [
                            ORDER_ID,
                            PRICE,
                            AMOUNT
                            ],
                            ...
                        ]
                    ]
            - updates : contain tick orders
                    [
                        CHANNEL_ID,
                        [
                            ORDER_ID,
                            PRICE,
                            AMOUNT
                        ]
                    ]
        """
        self._channel = None
        self._orderbook = orderbook

        #Used for debugging purposes allows us to replay historical ticks causing bugs
        self._log_ticks = False
        
        self._file = 'stream_logs.txt' if self._log_ticks else None



    def on_message(self, message) -> None:
        """
        Process incoming messages
        """
        print(message)

        #check types of messages

        if isinstance(message, dict):
            #we have some kind of event occuring ---> develope method to process this later

            if message['event'] == 'info':
                pass
            if message['event'] == 'subscribed':
                self._channel = message['chanId']
            return


        if isinstance(message, list):
            
            if self._log_ticks:
                #save the incoming data to log file
                with open(self._file, 'a') as file:
                    file.write(str(message)+'\n')

            # receiving orderbook information or check sum
            if message[1] == 'cs':
                #checksum message found - confirm our orderbook is correct
                self._orderbook.check_sum(message[2])

            if message[1] == 'hb':
                #heartbeat received ignore this
                return 

            if not len(message[1]) == 3:
                #initial snapshot recieved - create orderbook structure 
                self._orderbook.initialize_orderbook(message[1])

            else:
                item = message[1]
                order = Order(
                    id = item[0],
                    price = item[1],
                    side = Side.CALL if item[2] > 0 else Side.ASK, #delete order will have 0 quantity, side is UNK but this is handled by the qty
                    quantity = item[2] 
                )
                self._orderbook.process_order(order)
                


        return
        

    def _handle_checksum(self, cs_message:list):
        """
        Method to ensure our orderbook is correct by verifying a checksum match
        """
        #TODO this is the target 
        return

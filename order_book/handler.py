from order_book.orderbook import OrderBook


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
            # receiving orderbook information or check sum

            if message[1] == 'cs':
                #checksum message found - confirm our orderbook is correct
                self._handle_checksum(message)

            if message[1] == 'hb':
                #heartbeat received ignore this
                return 

            if not len(message[1]) == 3:
                #initial snapshot recieved - create orderbook structure 
                self._orderbook.initialize_orderbook(message[1])

            else:
                print(message)


        return
        

    def _handle_checksum(self, cs_message:list):
        """
        Method to ensure our orderbook is correct by verifying a checksum match
        """
        #TODO this is the target 
        return

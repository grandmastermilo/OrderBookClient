from order_book.orderbook import OrderBook


class Handler:

    def __init__(self, orderbook:OrderBook) -> None:
        """
        Handler constructor

        - used for processing messages for the orer
        """


    def on_message(self, message) -> None:
        """
        Process incoming messages
        """
        print(message)
        return
        
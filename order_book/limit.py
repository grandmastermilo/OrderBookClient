import os

from configurations import LOGGER


from order_book.order import Order
from order_book.side import Side



class Limit(object):

    def __init__(self, order:Order):
        """
        Limit Constructor

        - references: 
        -   https://arxiv.org/abs/1907.06230v1
        -   https://github.com/sadighian/crypto-rl

        - Defines price levels within the order book
        - Maintain information about a price level within the orderbook
        """

        # Main Limit attirbutes contain stats about the limit's current state
        self._price = order.price
        self._quantity = order.quantity
        self._count = 1
        self._side = order.side

        #list for storing orders in order of being created
        self._orders = [] 

        #TODO variables below are used primarily for tracking metrics fix after confirming the orderbook functionality
        self._notional = order.price*order.quantity
        

        #Limit historical statistics
        self._market_order_count = None
        self._market_order_quantity = None
        
        self._cancled_orders_count = None
        self._cancled_orders_qunatity = None

                

        return 

    @property
    def is_call(self) -> bool:
        """
        Imutable prop returns the side of the limit.
        """
        return self._side == Side.CALL


    def add_order(self, order:Order) -> None:
        """
        Method for appending orders to the FIFO order history.

        @param order: the incoming order to store in a FIFO system 
        """
        self._orders.append(order.id)


    def remove_order(self, order:Order) -> None:
        """
        Method to remove order from the FIFO order history

        - used for order canclation NOT order match

        @param order: the incoming order to store in a FIFO system 
        """
        self._orders.remove(order.id)

    


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
        self._side = order.side

        #list for storing orders in order of being created
        self._orders = [order.id] 

        #TODO variables below are used primarily for tracking metrics fix after confirming the orderbook functionality
        self._notional = order.price*order.quantity
        self._count = 1
        

        #Limit historical statistics
        self._market_order_count = None
        self._market_order_quantity = None
        
        self._cancled_orders_count = None
        self._cancled_orders_qunatity = None

                

        return 

    def __repr__(self):
        return f'price:{self._price}, side:{self._side}, quant:{self._quantity}'

    @property
    def is_call(self) -> bool:
        """
        Imutable prop returns the side of the limit.
        """
        return self._side == Side.CALL

    @property
    def is_unk(self) -> bool:
        """
        Imutable prop returns the side of the limit.
        """
        return self._side == Side.UNK

    @property
    def fifo_order(self) -> int:
        """
        Imutable, an order id for the fist order in the queue 
        """
        return self._orders[0]



    def add_order(self, order:Order) -> None:
        """
        Method for appending orders to the FIFO order history.

        @param order: the incoming order to store in a FIFO system 
        """
        self._orders.append(order.id)


    def pop_order(self) -> bool:
        """
        Method for consuming orders in FIFO

        @return: True if limit contains orders after the pop
        """
        if len(self._orders) == 1:
            #the last remaining order is consumed
            self._orders = []
            #convert the limit to unknown side
            self._side = Side.UNK
            
            return False
        
        else:
            self._orders = self._orders[1:]
            
            return True 



    def remove_order(self, order:Order) -> None:
        """
        Method to remove order from the FIFO order history

        - used for order canclation NOT order match

        @param order: 
        """

        if len(self._orders) == 1:
            self._orders.remove(order.id)
            #convert the limit to unknown side
            self._side = Side.UNK
            
            return False

        else:
            self._orders.remove(order.id)
            return True




    
    def switch(self, order:Order) -> None:
        """
        Method called for switching the limit side 

        occurs if the limit was cleared by incoming orders
        and the incoming orders take the limit 
        """
        self._orders.append(order.id)
        self._side = order.side
        self._quantity = order.quantity


    


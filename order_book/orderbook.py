from order_book.order import Order
from order_book.limit import Limit
from order_book.side import Side

from typing import Union,Dict

class OrderBook(object):

    def __init__(self):
        """
        OrderBook constructor 
        """

        self._all_orders:Dict[int, Order] = {} # order id

        self._limits:Dict[Union[int,float], Limit] = {} # price id

        self._best_ask = None
        self._best_call = None

        return

    def initialize_orderbook(self, snapshot:list) -> None:
        """
        Method for processing the initial repreentation of the orderbook provided from bitfinex 
        """
        
        for item in snapshot:
            
            #Check the orderbook works as expected
            if item[2] == 0:
                raise ("initialize_orderbook, unexpected error, initial snapshot should not contain 0 quantity orders.")

            order = Order(
                id = item[0],
                price = item[1],
                side = Side.CALL if item[2] > 0 else Side.ASK,
                quantity = item[2] 
                #TODO it may be more simple to make the quanitty absolute  
            )

            self._add_order(order)

        return

    def _add_order(self, order:Order) -> None:
        """
        Method to insert a new order 
        """
        # store order to OB history
        self._all_orders[order.id] = order

        # get limit 
        if order.price in self._limits.keys():

            # limit found
            # check limit side match
            if self._limits[order.price].is_call == order.is_call:
                #order matches
                self._limits[order.price].add_order(order)
            else:
                raise Exception(f"Add order exception: Order, Limit miss match, should not reach this point, orderid: {order.id}, price: {order.price}")

        else:
            #limit not found -- create and store limit
            limit = Limit(order)
            self._limits[order.price] = limit
      
        return

    def update_order(self, order:Order) -> None:
        """
        Method to update an order 
        """
        # retreive the previus order
        prev_order = self._all_orders[order.id]

        #order updates should not be in opposite side
        if not prev_order.is_call == order.is_call:
            raise Exception('update_order, Error when updating an order, side miss match')

        # update the order 
        prev_order.quantity = order.quantity

        #check for limit change
        if not prev_order.price == order.price:
            
            # remove order from limit
            self._limits[prev_order.price].remove_order(prev_order)
            #update order price
            prev_order.price = order.price
            
            #store the order in the correct limit
            self._add_order(prev_order)

        return

    def delete_order(self, order:Order) -> None:
        """
        Method to delete an order  
        """
        del self._all_orders[order.id]

        # assert the order price is stored in a limit
        if order.price in self._limits.keys():
            self._limits[order.price].remove_order(order)

        else:
            raise Exception("Delete order exception: Order price not a Limit, should not reach this point")

    def _process_match(self):
        """
        Method to determine if a market order was mad

        - checks for arrival of order that matches an opposing order 
        - matching incoming orders are filled (counted as market order)
        - order must be netted 
        - market orders that consume limit orders but consume orders FIFO 
        """
    
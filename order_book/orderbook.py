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


        #TODO orderbook statistics will be handled once the structure is verified
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

    def process_order(self, order:Order) -> None:
        """
        Method to handle incoming order, acts as a switch board to determine which action to take given the current orderbook and the order 
        """
        #quantity 0 requires deleting an existing order
        if order.quantity == 0:
            self._delete_order(order)
            return

        #check if the order exists and requires updating
        if order.id in self._all_orders.keys():
            self._update_order(order)


        # add order
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

            # retrieve the limit
            limit = self._limits[order.price]

            # check limit side match
            if limit.is_call == order.is_call:
                #order matches
                self._limits[order.price].add_order(order)
            elif limit.is_unk:
                #the limit exists but is empty
                limit.switch(order)
            else:
                # Market order has been made as opposing side
                self._process_match(order, limit)
                # raise Exception(f"Add order exception: Order, Limit miss match, should not reach this point, orderid: {order.id}, price: {order.price}")

        else:
            #limit not found -- create and store limit
            limit = Limit(order)
            self._limits[order.price] = limit
      
        return

    def _update_order(self, order:Order) -> None:
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

    def _delete_order(self, order:Order) -> None:
        """
        Method to delete an order  
        """
        del self._all_orders[order.id]

        # assert the order price is stored in a limit
        if order.price in self._limits.keys():
            self._limits[order.price].remove_order(order)

        else:
            raise Exception("Delete order exception: Order price not a Limit, should not reach this point")

    def _process_match(self, order:Order, limit:Limit):
        """
        Method to determine if a market order was mad
        - called when an incoming order matches an existing limit but on an opposing side

        - matching incoming orders are filled (counted as market order)
        - orders must be netted 
        - market orders that consume limit orders but consume orders FIFO 
        - limit can switch sides if all order in the limit are filled and the incoming orders net > 0
        """

        #until the incoming order has been consumed by existing limit orders
        while True:
            #TODO case incoming order has mass, limit is empty
            if limit.is_unk:
                #this is the case where a limit much switch sides
                limit.switch(order)
                break

            #retreive the first order in the limit 
            limit_order = self._all_orders[limit.fifo_order]

            if abs(limit_order.quantity) <= abs(order.quantity):
                
                #net the order quantity - note CALL/ASK have opsoing signs
                order.quantity += limit_order.quantity
                limit.pop_order()

                # remove the filled limit order from the book
                self._delete_order(limit_order)

                if order.quantity == 0:
                    # the market order has been filled
                    del self._all_orders[order.id]
                    break
                
            elif abs(limit_order.quantity) > abs(order.quantity):

                # net the existing limit order 
                limit_order.quantity += order.quantity
                
                del self._all_orders[order.id]
                break

    


    
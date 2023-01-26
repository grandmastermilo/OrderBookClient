import os
import sys
import inspect

root_dir = 'orderbook'
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
i = currentdir.rfind(root_dir)
sys.path.insert(0,currentdir[:i+len(root_dir)])

del i

import ast

from order_book.handler import Handler
from order_book.orderbook import OrderBook
from order_book.order import Order
from order_book.side import Side






def test_replay_checkum_failure():

    orderbook = OrderBook()
    handler = Handler(orderbook=orderbook) 

    with open('./test/stream_logs.txt', 'r') as f:
    
        data = f.readlines()

    for i, message in enumerate(data):
        print(i)
        message = ast.literal_eval((message))

       

        if len(message[1]) == 3:
            item = message[1]
            order = Order(
                id = item[0],
                price = item[1],
                side = Side.CALL if item[2] > 0 else Side.ASK, #delete order will have 0 quantity, side is UNK but this is handled by the qty
                quantity = item[2] 
            )


            #determine if the order if add, update, remove

            # DELETE
            if order.price == 0:
                #process the message
                handler.on_message(message)

                #not in orderbook storage
                assert order.id not in orderbook._all_orders.keys()

                #check for limit stores
                for limit in orderbook._limits.keys():
                    assert order.id not in orderbook._limits[limit]._orders


            #UPDATE
            elif order.id in orderbook._all_orders.keys():
                #get inital order details
                prev_price = orderbook._all_orders[order.id].price
                prev_q = orderbook._all_orders[order.id].quantity

                #process order
                handler.on_message(message)

                #change of price
                if not order.price == prev_price:
                    
                    #ensure price update has happended 
                    assert orderbook._all_orders[order.id].price == order.price
                    assert not order.id in orderbook._limits[prev_price]._orders
                    assert order.id in orderbook._limits[order.price]._orders

            else:
                #process order
                handler.on_message(message)




        else:

            handler.on_message(message)
        

        
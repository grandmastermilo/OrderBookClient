import os
import sys
import inspect

root_dir = 'orderbook'
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
i = currentdir.rfind(root_dir)
sys.path.insert(0,currentdir[:i+len(root_dir)])

del i


from order_book.orderbook import OrderBook
from order_book.order import Order
from order_book.side import Side


import pytest


def test_load_snapshot():

    orderbook = OrderBook()
    snapshot =  [[1, 2222, 0.1], [2, 2223, 0.2], [3,2223, 0.3], [4, 2224, -0.1]]

    orderbook.initialize_orderbook(snapshot)

    assert sorted(orderbook._all_orders.keys()) == [1, 2, 3, 4]
    assert sorted(orderbook._limits.keys()) == [2222,2223, 2224]

    assert orderbook._all_orders[1].price == 2222

    assert orderbook._limits[2222]._orders == [1]
    assert orderbook._limits[2223]._orders == [2,3]



def test_add_order():

    orderbook = OrderBook()
    snapshot =  [[1, 2222, 0.1], [2, 2223, 0.2], [3,2223, 0.3], [4, 2224, -0.1]]

    orderbook.initialize_orderbook(snapshot)

    order = Order(
        id = 5, price=2225, side=Side.ASK, quantity=-0.1
    )

    orderbook._add_order(order)

    # CASE 1 ------------------------------------ order new limit
    assert 2225 in orderbook._limits.keys()
    assert 5 in orderbook._all_orders.keys()


    order = Order(
        id = 6, price=2222, side=Side.CALL, quantity=-0.1
    )

    orderbook._add_order(order)

    # CASE 2 ------------------------------------ order existing limit
    assert 6 in orderbook._all_orders.keys()
    assert sorted(orderbook._limits[2222]._orders) == [1, 6]



def test_update_order():

    return





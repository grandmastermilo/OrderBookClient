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
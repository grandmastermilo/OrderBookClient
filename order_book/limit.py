import os
from enum import Enum
from configurations import LOGGER


class Side(Enum):
    """
    Enum defining this side of the limit 
    """
    Unknown = 0
    Bid = 1
    Ask = 2


class Limit(object):

    def __init__(self):
        """
        Limit Constructor

        - references: 
        -   https://arxiv.org/abs/1907.06230v1
        -   https://github.com/sadighian/crypto-rl

        - Defines price levels within the order book
        - Maintain information about a price level within the orderbook
        """

        # Main Limit attirbutes contain stats about the 
        self._price = None
        self._quantity = None
        self._count = None
        self._notional = None
        self._side = None

        return 


from dataclasses import dataclass

from order_book.side import Side

@dataclass
class Order:
    """
    Order class for consuming order messages from the socket api's
    """
    id: str
    price: float
    side:Side
    quantity: int = 0

    @property
    def _notional(self) -> float:
        return self.price * self.quantity

    @property
    def is_call(self) -> bool:
        """
        imutable prop returns the side of the order  
        """
        return self.side == Side.CALL
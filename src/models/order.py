# src/models/order.py

class Order:
    """
    Класс для представления ордера.
    """
    def __init__(self, symbol, side, type, quantity, price=None):
        self.symbol = symbol
        self.side = side
        self.type = type
        self.quantity = quantity
        self.price = price
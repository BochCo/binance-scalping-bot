# src/models/position.py

class Position:
    """
    Класс для представления позиции.
    """
    def __init__(self, symbol, side, quantity, entry_price):
        self.symbol = symbol
        self.side = side
        self.quantity = quantity
        self.entry_price = entry_price
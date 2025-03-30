# src/models/market_data.py

class MarketData:
    """
    Класс для представления данных о рынке.
    """
    def __init__(self, symbol, price, volume):
        self.symbol = symbol
        self.price = price
        self.volume = volume
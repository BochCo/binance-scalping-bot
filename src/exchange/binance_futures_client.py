# src/exchange/binance_futures_client.py

from src.exchange.exchange_client import BaseExchangeClient

class BinanceFuturesClient(BaseExchangeClient):
    """
    Клиент для взаимодействия с фьючерсным API Binance.
    """
    def __init__(self, api_key, api_secret):
        super().__init__(api_key, api_secret)
        # Binance Futures specific initialization
        pass

    def place_order(self, symbol, side, type, quantity, price=None):
        # Binance Futures implementation
        print("BinanceFuturesClient: place_order() not implemented yet")
        pass

    def get_market_data(self, symbol):
        # Binance Futures implementation
        print("BinanceFuturesClient: get_market_data() not implemented yet")
        pass

    def get_balance(self, asset):
        # Binance Futures implementation
        print("BinanceFuturesClient: get_balance() not implemented yet")
        pass

    def cancel_order(self, order_id, symbol):
        # Binance Futures implementation
        print("BinanceFuturesClient: cancel_order() not implemented yet")
        pass
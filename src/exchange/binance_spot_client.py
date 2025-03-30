# src/exchange/binance_spot_client.py

from src.exchange.exchange_client import BaseExchangeClient

class BinanceSpotClient(BaseExchangeClient):
    """
    Клиент для взаимодействия со спотовым API Binance.
    """
    def __init__(self, api_key, api_secret):
        super().__init__(api_key, api_secret)
        # Binance Spot specific initialization
        pass

    def place_order(self, symbol, side, type, quantity, price=None):
        # Binance Spot implementation
        print("BinanceSpotClient: place_order() not implemented yet")
        pass

    def get_market_data(self, symbol):
        # Binance Spot implementation
        print("BinanceSpotClient: get_market_data() not implemented yet")
        pass

    def get_balance(self, asset):
        # Binance Spot implementation
        print("BinanceSpotClient: get_balance() not implemented yet")
        pass

    def cancel_order(self, order_id, symbol):
        # Binance Spot implementation
        print("BinanceSpotClient: cancel_order() not implemented yet")
        pass
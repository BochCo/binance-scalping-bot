# src/exchange/bybit_spot_client.py

from src.exchange.exchange_client import BaseExchangeClient

class BybitSpotClient(BaseExchangeClient):
    """
    Клиент для взаимодействия со спотовым API Bybit.
    """
    def __init__(self, api_key, api_secret):
        super().__init__(api_key, api_secret)
        # Bybit Spot specific initialization
        pass

    def place_order(self, symbol, side, type, quantity, price=None):
        # Bybit Spot implementation
        print("BybitSpotClient: place_order() not implemented yet")
        pass

    def get_market_data(self, symbol):
        # Bybit Spot implementation
        print("BybitSpotClient: get_market_data() not implemented yet")
        pass

    def get_balance(self, asset):
        # Bybit Spot implementation
        print("BybitSpotClient: get_balance() not implemented yet")
        pass

    def cancel_order(self, order_id, symbol):
        # Bybit Spot implementation
        print("BybitSpotClient: cancel_order() not implemented yet")
        pass
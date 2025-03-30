# bot.py

import requests
from config import API_KEY, API_SECRET, BASE_URL
from utils import prepare_request

class Bot:
    def __init__(self):
        self.base_url = BASE_URL
        self.api_key = API_KEY
        self.api_secret = API_SECRET
    
    def get_market_data(self, symbol):
        """
        Получение данных о рынке.
        """
        endpoint = "/v5/market/tickers"
        params = {"category": "linear", "symbol": symbol}
        
        response = requests.get(self.base_url + endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка при получении данных о рынке: {response.text}")
    
    def get_balance(self, coin="USDT"):
        """
        Получение баланса.
        """
        endpoint = "/v5/account/wallet-balance"
        payload = {
            "accountType": "UNIFIED",
            "category": "linear",
            "coin": coin
        }
        
        headers, raw_body = prepare_request(self.api_key, self.api_secret, endpoint, payload=payload)
        response = requests.post(self.base_url + endpoint, headers=headers, data=raw_body)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка при получении баланса: {response.text}")
    
    def place_order(self, symbol, side, order_type, qty, price=None):
        """
        Размещение ордера.
        """
        endpoint = "/v5/order/create"
        payload = {
            "category": "linear",
            "symbol": symbol,
            "side": side.capitalize(),
            "orderType": order_type.capitalize(),
            "qty": str(qty),
            "timeInForce": "GTC"
        }
        
        if order_type.lower() == "limit" and price:
            payload["price"] = str(price)
        
        headers, raw_body = prepare_request(self.api_key, self.api_secret, endpoint, payload=payload)
        response = requests.post(self.base_url + endpoint, headers=headers, data=raw_body)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка при размещении ордера: {response.text}")
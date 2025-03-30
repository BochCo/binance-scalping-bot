# src/exchange/bybit_futures_client.py

import requests
import time
from src.exchange.exchange_client import BaseExchangeClient
import urllib.parse

class BybitFuturesClient(BaseExchangeClient):
    """
    Клиент для взаимодействия с фьючерсным API Bybit.
    """
    def __init__(self, api_key, api_secret, use_testnet=True):
        """
        Инициализация клиента.

        Args:
            api_key (str): API ключ.
            api_secret (str): Секретный ключ.
            use_testnet (bool): Использовать тестовую сеть (True) или реальную (False).
        """
        super().__init__(api_key, api_secret)
        self.base_url = "https://api-testnet.bybit.com" if use_testnet else "https://api.bybit.com" # Базовый URL для API Bybit
        self.use_testnet = use_testnet

    def place_order(self, symbol, side, type, quantity, price=None):
        """
        Размещает ордер на бирже.

        Args:
            symbol (str): Символ торгуемой пары (например, BTCUSDT).
            side (str): Сторона ордера (BUY или SELL).
            type (str): Тип ордера (MARKET или LIMIT).
            quantity (float): Количество для покупки/продажи.
            price (float, optional): Цена ордера (для LIMIT ордеров). Defaults to None.

        Returns:
            dict: Ответ от API в формате JSON.
        """
        endpoint = "/v2/private/order/create" # Конечная точка API для размещения ордера
        url = self.base_url + endpoint
        timestamp = str(int(time.time() * 1000))
        params = {
            "symbol": symbol,
            "side": side,
            "order_type": type.upper(),  # Bybit требует верхний регистр
            "qty": quantity,
            "price": price, # Обязательно для Limit ордеров
            "time_in_force": "GoodTillCancel", # Или "ImmediateOrCancel", "FillOrKill",
            "timestamp": timestamp,
            "api_key": self.api_key
        }
        params['sign'] = self._generate_signature(params)
        
        headers = {
            "Content-Type": "application/json"
        }
        self._rate_limit() # Применяем ограничение скорости
        response = requests.post(url, headers=headers, json=params)
        return self._handle_response(response)

    def get_market_data(self, symbol):
        """
        Получает данные о рынке (текущую цену).

        Args:
            symbol (str): Символ торгуемой пары (например, BTCUSDT).

        Returns:
            dict: Ответ от API в формате JSON.
        """
        endpoint = "/v2/public/tickers"  # Конечная точка API для получения данных о рынке
        url = f"{self.base_url}{endpoint}?symbol={symbol}"
        self._rate_limit() # Применяем ограничение скорости
        response = requests.get(url)
        return self._handle_response(response)

    def get_balance(self, asset):
        """
        Получает баланс аккаунта.

        Args:
            asset (str): Символ валюты (например, USDT).

        Returns:
            dict: Ответ от API в формате JSON.
        """
        endpoint = "/v2/private/wallet/balance" # Конечная точка API для получения баланса
        timestamp = str(int(time.time() * 1000))
        params = {
            "coin": asset,
            "timestamp": timestamp,
            "api_key": self.api_key
        }
        params['sign'] = self._generate_signature(params)

        headers = {
            "Content-Type": "application/json"
        }
        self._rate_limit() # Применяем ограничение скорости
        response = requests.get(url, headers=headers, params=params)
        return self._handle_response(response)

    def cancel_order(self, order_id, symbol):
        """
        Отменяет ордер.

        Args:
            order_id (str): ID ордера.
            symbol (str): Символ торгуемой пары (например, BTCUSDT).

        Returns:
            dict: Ответ от API в формате JSON.
        """
        endpoint = "/v2/private/order/cancel" # Конечная точка API для отмены ордера
        url = self.base_url + endpoint
        timestamp = str(int(time.time() * 1000))
        params = {
            "symbol": symbol,
            "order_id": order_id,
            "timestamp": timestamp,
            "api_key": self.api_key
        }
        params['sign'] = self._generate_signature(params)

        headers = {
            "Content-Type": "application/json"
        }
        self._rate_limit() # Применяем ограничение скорости
        response = requests.post(url, headers=headers, json=params)
        return self._handle_response(response)
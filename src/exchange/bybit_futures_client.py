# src/exchange/bybit_futures_client.py

import requests
import time
from src.exchange.exchange_client import BaseExchangeClient
import urllib.parse
import json

class BybitFuturesClient(BaseExchangeClient):
    """
    Клиент для взаимодействия с фьючерсным API Bybit.
    """
    def __init__(self, api_key, api_secret, base_url):
        """
        Инициализация клиента.

        Args:
            api_key (str): API ключ.
            api_secret (str): Секретный ключ.
            base_url (str): Базовый URL для API (Testnet или Mainnet).
        """
        super().__init__(api_key, api_secret)
        self.base_url = base_url

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
        endpoint = "/v5/order/create"  # Обновленный эндпоинт для API v5
        url = self.base_url + endpoint
        timestamp = str(int(time.time() * 1000))
        recv_window = 5000 # Recommended
        params = {
            "symbol": symbol,
            "side": side.capitalize(),  # Bybit требует CamelCase
            "orderType": type.capitalize(),  # Bybit требует CamelCase
            "qty": str(quantity),  # Bybit требует строку
            "price": str(price) if price else None,  # Bybit требует строку, только для LIMIT
            "timeInForce": "GoodTillCancel",  # Или "ImmediateOrCancel", "FillOrKill"
            "category": "linear",
            "accountType": "UNIFIED" # Добавляем тип аккаунта
        }
        if price is None:
            del params["price"] # Price не нужен для MARKET ордеров

        # Sort parameters alphabetically
        sorted_params = dict(sorted(params.items()))
        raw_body = json.dumps(sorted_params, separators=(',', ':'))

        signature = self._generate_signature(self.api_secret, timestamp, self.api_key, recv_window, endpoint, raw_body)

        headers = {
            "Content-Type": "application/json",
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-SIGN": signature,
			"X-BAPI-RECV-WINDOW": str(recv_window)
        }

        self._rate_limit()  # Применяем ограничение скорости
        response = requests.post(url, headers=headers, data=raw_body)
        return self._handle_response(response)

    def get_market_data(self, symbol):
        """
        Получает данные о рынке (текущую цену).

        Args:
            symbol (str): Символ торгуемой пары (например, BTCUSDT).

        Returns:
            dict: Ответ от API в формате JSON.
        """
        endpoint = "/v5/market/tickers"  # Обновленный эндпоинт для API v5
        category = "linear"  # Указываем категорию
        url = f"{self.base_url}{endpoint}?symbol={symbol}&category={category}"
        self._rate_limit()  # Применяем ограничение скорости
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
        endpoint = "/v5/account/wallet-balance"  # Обновленный эндпоинт для API v5
        url = self.base_url + endpoint
        timestamp = str(int(time.time() * 1000))
        recv_window = 5000
        params = {
            "coin": asset,
            "timestamp": timestamp,
            "api_key": self.api_key,
            "accountType": "UNIFIED",  # Изменяем тип аккаунта
            "category": "linear"  # Добавляем категорию
        }
        
        # Sort parameters alphabetically
        sorted_params = dict(sorted(params.items()))
        raw_body = json.dumps(sorted_params, separators=(',', ':'))

        signature = self._generate_signature(self.api_secret, timestamp, self.api_key, recv_window, endpoint, raw_body)

        headers = {
            "Content-Type": "application/json",
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-SIGN": signature,
            "X-BAPI-RECV-WINDOW": str(recv_window)
        }

        self._rate_limit()  # Применяем ограничение скорости
        response = requests.post(url, headers=headers, data=raw_body)
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
        # TODO: Implement cancel order with API v5
        endpoint = "/v2/private/order/cancel"  # Оставляем пока без изменений
        url = self.base_url + endpoint
        timestamp = str(int(time.time() * 1000))
        params = {
            "symbol": symbol,
            "order_id": order_id,
            "timestamp": timestamp,
            "api_key": self.api_key
        }
        params['sign'] = self._generate_signature(self.api_secret, timestamp, self.api_key, 5000, endpoint, params)

        headers = {
            "Content-Type": "application/json"
        }
        self._rate_limit()  # Применяем ограничение скорости
        response = requests.post(url, headers=headers, json=params)
        return self._handle_response(response)
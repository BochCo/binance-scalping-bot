# src/exchange/exchange_client.py

from abc import ABC, abstractmethod
import time
import requests
import hashlib
import hmac
import urllib.parse
import json

class IExchangeClient(ABC):
    """
    Интерфейс для клиентов бирж.
    """
    @abstractmethod
    def place_order(self, symbol, side, type, quantity, price=None):
        pass

    @abstractmethod
    def get_market_data(self, symbol):
        pass

    @abstractmethod
    def get_balance(self, asset):
        pass

    @abstractmethod
    def cancel_order(self, order_id, symbol):
        pass


class BaseExchangeClient(IExchangeClient):
    """
    Базовый класс для клиентов бирж.
    """
    def __init__(self, api_key, api_secret):
        """
        Инициализация клиента.

        Args:
            api_key (str): API ключ.
            api_secret (str): Секретный ключ.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.rate_limit_delay = 0.1  # Задержка между запросами (в секундах)

    def _handle_response(self, response):
        """
        Обрабатывает ответ от API.

        Args:
            response (requests.Response): Ответ от API.

        Returns:
            dict: Ответ от API в формате JSON.

        Raises:
            Exception: Если произошла ошибка.
        """
        try:
            response.raise_for_status()  # Проверка на HTTP ошибки
            data = response.json()
            if 'retCode' in data and data['retCode'] != 0: # Проверка на ошибки Bybit
                raise Exception(f"Ошибка API: {data['retCode']} - {data['retMsg']}")
            return data
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP ошибка: {e}")
        except Exception as e:
            raise Exception(f"Ошибка при обработке ответа: {e}")

    def _rate_limit(self):
        """
        Реализует ограничение скорости запросов.
        """
        time.sleep(self.rate_limit_delay)

    def _generate_signature(self, api_secret, timestamp, api_key, recv_window, endpoint, raw_body):
        """
        Генерирует подпись для запроса к API Bybit v5.

        Args:
            api_secret (str): Секретный ключ API.
            timestamp (str): Timestamp запроса.
            api_key (str): API ключ.
            recv_window (str): recv_window
            endpoint (str): Endpoint запроса
            raw_body (str): raw_body

        Returns:
            str: Подпись запроса.
        """
        sign_str = str(timestamp) + api_key + str(recv_window) + raw_body
        print(f"_generate_signature - sign_str: {sign_str}")
        hash = hmac.new(api_secret.encode("utf-8"), sign_str.encode("utf-8"), hashlib.sha256)
        signature = hash.hexdigest()
        print(f"_generate_signature - signature: {signature}")
        return signature
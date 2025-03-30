# src/exchange/exchange_client.py

from abc import ABC, abstractmethod
import time
import requests
import hashlib
import hmac
import urllib.parse

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
            if 'ret_code' in data and data['ret_code'] != 0: # Проверка на ошибки Bybit
                raise Exception(f"Ошибка API: {data['ret_code']} - {data['ret_msg']}")
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

    def _generate_signature(self, params):
        """
        Генерирует подпись для запроса к API Bybit.

        Args:
            params (dict): Параметры запроса.

        Returns:
            str: Подпись запроса.
        """
        query_string = urllib.parse.urlencode(sorted(params.items(), key=lambda x: x[0]))
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return signature
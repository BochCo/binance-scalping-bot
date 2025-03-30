import time
import hmac
import hashlib
import json
from typing import Dict, Tuple
from config import REQUEST_DELAY

class AuthHelper:
    """Класс для работы с аутентификацией API"""
    
    @staticmethod
    def generate_signature(secret: str, message: str) -> str:
        """
        Генерация подписи HMAC-SHA256
        
        Args:
            secret: Секретный ключ API
            message: Строка для подписи
            
        Returns:
            Сгенерированная подпись
        """
        return hmac.new(
            secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    @staticmethod
    def prepare_request(
        api_key: str,
        secret: str,
        method: str,
        endpoint: str,
        params: Dict = None
    ) -> Tuple[Dict, str]:
        """
        Подготовка авторизованного запроса к API
        
        Args:
            api_key: Ключ API
            secret: Секретный ключ
            method: HTTP метод (GET/POST)
            endpoint: Конечная точка API
            params: Параметры запроса
            
        Returns:
            Кортеж (headers, body): заголовки и тело запроса
        """
        timestamp = str(int(time.time() * 1000))  # Текущая метка времени
        recv_window = "5000"  # Окно получения данных
        params = params or {}

        # Для GET-запросов параметры должны быть в URL и отсортированы
        if method == "GET":
            param_str = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
            message = f"{timestamp}{api_key}{recv_window}{param_str}"
            body = ""
        else:
            # Для POST - параметры в теле запроса
            body = json.dumps(params, separators=(',', ':'))
            message = f"{timestamp}{api_key}{recv_window}{body}"

        # Генерация подписи
        signature = AuthHelper.generate_signature(secret, message)

        # Формирование заголовков
        headers = {
            "X-BAPI-API-KEY": api_key,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-SIGN": signature,
            "X-BAPI-RECV-WINDOW": recv_window,
            "Content-Type": "application/json"
        }

        # Задержка для соблюдения rate limit
        time.sleep(REQUEST_DELAY)
        return headers, body
# utils.py

import time
import hmac
import hashlib
import json

def generate_signature(secret_key, message):
    """
    Генерация подписи HMAC-SHA256 для Bybit API.
    """
    return hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def prepare_request(api_key, secret_key, endpoint, method="POST", payload=None):
    """
    Подготовка запроса к Bybit API V5.
    """
    timestamp = str(int(time.time() * 1000))
    recv_window = "5000" # По умолчанию 5000, можно увеличить при необходимости

    if payload is None:
        payload = {}

    # Для POST-запросов с JSON тело не сортируется
    # Для GET-запросов параметры сортируются (здесь не реализовано, т.к. пока не используется)
    # Преобразуем payload в JSON строку "как есть"
    raw_body = json.dumps(payload, separators=(',', ':'))

    # Формируем строку для подписи (timestamp + apiKey + recvWindow + requestBody)
    message = f"{timestamp}{api_key}{recv_window}{raw_body}"
    signature = generate_signature(secret_key, message)

    # Формируем заголовки
    headers = {
        "X-BAPI-API-KEY": api_key,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-SIGN": signature,
        "X-BAPI-RECV-WINDOW": recv_window, # Добавляем recv_window в заголовки
        "Content-Type": "application/json"
    }

    # Возвращаем заголовки и тело запроса (для POST)
    return headers, raw_body
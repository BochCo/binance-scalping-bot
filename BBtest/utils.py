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
    Подготовка запроса к Bybit API.
    """
    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"
    
    if payload is None:
        payload = {}
    
    # Добавляем обязательные параметры
    payload.update({
        "api_key": api_key,
        "timestamp": timestamp
    })
    
    # Сортируем параметры по алфавиту
    sorted_payload = dict(sorted(payload.items()))
    raw_body = json.dumps(sorted_payload, separators=(',', ':'))
    
    # Формируем строку для подписи
    message = f"{timestamp}{api_key}{recv_window}{raw_body}"
    signature = generate_signature(secret_key, message)
    
    # Формируем заголовки
    headers = {
        "X-BAPI-API-KEY": api_key,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-SIGN": signature,
        "Content-Type": "application/json"
    }
    
    return headers, raw_body
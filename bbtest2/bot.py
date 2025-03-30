import time
import requests
import logging
from typing import Dict, Optional, List
from config import (
    BASE_URL, API_KEY, API_SECRET, MAX_RETRIES,
    SYMBOL, MIN_ORDER_SIZE, POSITION_SIZE,
    REQUEST_TIMEOUT, ORDER_STATUS_TIMEOUT,
    ORDER_CANCEL_DELAY, ERROR_RETRY_DELAY
)
from utils import AuthHelper

class BybitTradingBot:
    """Класс для взаимодействия с API Bybit"""
    
    def __init__(self, demo_mode: bool = True):
        self.base_url = BASE_URL
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.demo_mode = demo_mode
        self.session = requests.Session()
        
        if demo_mode and "api-demo" not in self.base_url:
            raise ValueError("Для демо-режима должен использоваться api-demo.bybit.com")

    def _send_request(self, method: str, endpoint: str, params: Dict = None) -> Dict:
        """Отправка авторизованного запроса к API"""
        for attempt in range(MAX_RETRIES):
            try:
                headers, data = AuthHelper.prepare_request(
                    self.api_key,
                    self.api_secret,
                    method,
                    endpoint,
                    params
                )

                timeout = ORDER_STATUS_TIMEOUT if "order" in endpoint.lower() else REQUEST_TIMEOUT

                response = self.session.request(
                    method,
                    self.base_url + endpoint,
                    headers=headers,
                    params=params if method == "GET" else None,
                    data=data if method == "POST" else None,
                    timeout=timeout
                )

                response.raise_for_status()
                result = response.json()

                if result.get('retCode') != 0:
                    raise Exception(f"API error: {result.get('retMsg')}")

                return result

            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    raise
                time.sleep(ERROR_RETRY_DELAY)

    # Методы для работы с аккаунтом
    def get_balance(self, coin: str = "USDT") -> Dict:
        """Получение баланса по конкретной монете"""
        return self._send_request(
            "GET",
            "/v5/account/wallet-balance",
            {"accountType": "UNIFIED", "coin": coin}
        )

    def get_account_info(self) -> Dict:
        """Получение информации об аккаунте"""
        return self._send_request("GET", "/v5/account/info")

    # Методы для работы с рынком
    def get_orderbook(self, symbol: str = SYMBOL, depth: int = 25) -> Dict:
        """Получение стакана цен"""
        return self._send_request(
            "GET",
            "/v5/market/orderbook",
            {"category": "linear", "symbol": symbol, "limit": depth}
        )

    def get_ticker(self, symbol: str = SYMBOL) -> Dict:
        """Получение текущих цен"""
        return self._send_request(
            "GET",
            "/v5/market/tickers",
            {"category": "linear", "symbol": symbol}
        )

    # Методы для работы с ордерами
    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        qty: float,
        price: Optional[float] = None,
        reduce_only: bool = False
    ) -> Dict:
        """Размещение нового ордера"""
        if qty < MIN_ORDER_SIZE:
            raise ValueError(f"Минимальный объем ордера: {MIN_ORDER_SIZE}")

        payload = {
            "category": "linear",
            "symbol": symbol,
            "side": side.capitalize(),
            "orderType": order_type.capitalize(),
            "qty": str(round(qty, 8)),
            "timeInForce": "GTC",
            "reduceOnly": reduce_only
        }

        if order_type.lower() == "limit" and price:
            payload["price"] = str(round(price, 2))

        return self._send_request("POST", "/v5/order/create", payload)

    def cancel_order(self, order_id: str, symbol: str = SYMBOL) -> Dict:
        """Отмена активного ордера с указанием символа"""
        return self._send_request(
            "POST",
            "/v5/order/cancel",
            {
                "category": "linear",
                "symbol": symbol,  # Добавляем обязательный параметр symbol
                "orderId": order_id
            }
        )

    def get_active_orders(self, symbol: str = SYMBOL) -> Dict:
        """Получение списка активных ордеров"""
        return self._send_request(
            "GET",
            "/v5/order/realtime",
            {"category": "linear", "symbol": symbol}
        )

    def get_order_history(self, order_id: str = None, symbol: str = SYMBOL) -> Dict:
        """Получение истории ордеров"""
        params = {"category": "linear", "symbol": symbol}
        if order_id:
            params["orderId"] = order_id
        return self._send_request("GET", "/v5/order/history", params)

    # Методы для работы с позициями
    def get_positions(self, symbol: str = SYMBOL) -> Dict:
        """Получение текущих позиций"""
        return self._send_request(
            "GET",
            "/v5/position/list",
            {"category": "linear", "symbol": symbol}
        )

    def set_leverage(self, symbol: str, leverage: int) -> Dict:
        """Установка плеча для позиции"""
        return self._send_request(
            "POST",
            "/v5/position/set-leverage",
            {
                "category": "linear",
                "symbol": symbol,
                "buyLeverage": str(leverage),
                "sellLeverage": str(leverage)
            }
        )
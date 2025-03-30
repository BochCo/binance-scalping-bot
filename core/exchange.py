from binance.client import Client

class BinanceExchange:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

    def get_current_price(self, symbol):
        """Получает текущую цену для указанного символа."""
        try:
            ticker = self.client.get_ticker(symbol=symbol)
            return float(ticker['lastPrice'])
        except Exception as e:
            print(f"Ошибка при получении цены {symbol}: {e}")
            return None

    def buy_market_order(self, symbol, quantity):
        """Размещает рыночный ордер на покупку."""
        try:
            order = self.client.order_market_buy(symbol=symbol, quantity=quantity)
            print(f"Куплено {quantity} {symbol} по рыночной цене. Order ID: {order['orderId']}")
            return order
        except Exception as e:
            print(f"Ошибка при покупке {symbol}: {e}")
            return None

    def sell_market_order(self, symbol, quantity):
        """Размещает рыночный ордер на продажу."""
        try:
            order = self.client.order_market_sell(symbol=symbol, quantity=quantity)
            print(f"Продано {quantity} {symbol} по рыночной цене. Order ID: {order['orderId']}")
            return order
        except Exception as e:
            print(f"Ошибка при продаже {symbol}: {e}")
            return None

    def get_account_balance(self):
        """Получает баланс аккаунта."""
        try:
            account = self.client.get_account()
            return account
        except Exception as e:
            print(f"Ошибка при получении баланса аккаунта: {e}")
            return None

    def get_symbol_info(self, symbol):
        """Получает информацию о символе (например, шаг цены и шаг количества)."""
        try:
            info = self.client.get_symbol_info(symbol)
            return info
        except Exception as e:
            print(f"Ошибка при получении информации о символе {symbol}: {e}")
            return None
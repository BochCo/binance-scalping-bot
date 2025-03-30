import time
import logging
from bot import BybitTradingBot
from config import (
    SYMBOL, POSITION_SIZE, MAX_SPREAD_PCT,
    MAX_ACTIVE_ORDERS, ORDER_CANCEL_DELAY
)

class TradingStrategy:
    """Класс реализующий торговую стратегию"""
    
    def __init__(self):
        self.bot = BybitTradingBot(demo_mode=True)
        self.symbol = SYMBOL
        self.position_size = POSITION_SIZE
        self.max_spread_pct = MAX_SPREAD_PCT
        self.max_active_orders = MAX_ACTIVE_ORDERS
        self.active_order_ids = []

    def cleanup_old_orders(self):
        """Отмена старых неисполненных ордеров с обработкой ошибок"""
        try:
            current_orders = self.bot.get_active_orders(self.symbol)
            current_order_ids = [o['orderId'] for o in current_orders.get('result', {}).get('list', [])]
            
            for order_id in self.active_order_ids[:]:
                if order_id not in current_order_ids:
                    self.active_order_ids.remove(order_id)
                    continue
                
                try:
                    time.sleep(ORDER_CANCEL_DELAY)
                    cancel_result = self.bot.cancel_order(order_id, self.symbol)
                    if cancel_result['retCode'] == 0:
                        self.active_order_ids.remove(order_id)
                        logging.info(f"Ордер отменён: {order_id}")
                    else:
                        logging.error(f"Ошибка отмены ордера {order_id}: {cancel_result['retMsg']}")
                except Exception as e:
                    logging.error(f"Ошибка при отмене ордера {order_id}: {str(e)}")
                    time.sleep(ERROR_RETRY_DELAY)
        except Exception as e:
            logging.error(f"Ошибка в процессе отмены ордеров: {str(e)}")

    def execute_strategy(self):
        """Основная логика торговой стратегии"""
        try:
            # Проверка активных ордеров
            if len(self.active_order_ids) >= self.max_active_orders:
                self.cleanup_old_orders()
                return

            # Получение баланса
            balance = self.bot.get_balance()
            usdt_balance = float(balance['result']['list'][0]['coin'][0]['equity'])
            logging.info(f"Текущий баланс: {usdt_balance:.2f} USDT")

            # Получение рыночных данных
            orderbook = self.bot.get_orderbook()
            best_bid = float(orderbook['result']['b'][0][0])
            best_ask = float(orderbook['result']['a'][0][0])
            spread = (best_ask - best_bid) / best_ask * 100
            logging.info(f"Рынок: Bid={best_bid:.2f} | Ask={best_ask:.2f} | Спред={spread:.4f}%")

            # Условия для входа
            if spread < self.max_spread_pct:
                order_price = round(best_bid * 0.999, 2)
                order = self.bot.place_order(
                    symbol=self.symbol,
                    side="Buy",
                    order_type="Limit",
                    qty=self.position_size,
                    price=order_price
                )
                
                if order['retCode'] == 0:
                    order_id = order['result']['orderId']
                    self.active_order_ids.append(order_id)
                    logging.info(f"Ордер размещён | ID: {order_id} | Цена: {order_price} | Объём: {self.position_size}")
                else:
                    logging.error(f"Ошибка при размещении ордера: {order['retMsg']}")
            else:
                logging.info(f"Спред {spread:.4f}% слишком высок, пропускаем сделку")

        except Exception as e:
            logging.error(f"Ошибка в стратегии: {str(e)}", exc_info=True)

def setup_logging():
    """Настройка системы логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("trading_bot.log"),
            logging.StreamHandler()
        ]
    )

if __name__ == "__main__":
    setup_logging()
    strategy = TradingStrategy()
    
    try:
        logging.info("Запуск торгового бота...")
        while True:
            strategy.execute_strategy()
            time.sleep(10)
    except KeyboardInterrupt:
        logging.info("Бот остановлен пользователем")
    finally:
        logging.info("Отмена всех активных ордеров...")
        for order_id in strategy.active_order_ids:
            try:
                strategy.bot.cancel_order(order_id, strategy.symbol)
            except Exception as e:
                logging.error(f"Ошибка при отмене ордера {order_id}: {str(e)}")
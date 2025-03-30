from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()

# Настройки API Bybit
BASE_URL = os.getenv("BASE_URL", "https://api-demo.bybit.com")  # Базовый URL API
API_KEY = os.getenv("API_KEY")  # API ключ
API_SECRET = os.getenv("API_SECRET")  # Секретный ключ API

# Параметры торговли
SYMBOL = os.getenv("SYMBOL", "BTCUSDT")  # Торговая пара
MIN_ORDER_SIZE = float(os.getenv("MIN_ORDER_SIZE", 0.001))  # Минимальный объем ордера
POSITION_SIZE = float(os.getenv("POSITION_SIZE", 0.001))  # Размер позиции
MAX_SPREAD_PCT = float(os.getenv("MAX_SPREAD_PCT", 0.05))  # Максимальный спред для входа (в %)
MAX_ACTIVE_ORDERS = int(os.getenv("MAX_ACTIVE_ORDERS", 3))  # Макс. количество активных ордеров

# Настройки запросов
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))  # Макс. попыток запроса
REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", 0.1))  # Задержка между запросами (в сек)
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))  # Таймаут запросов (в сек)
ORDER_STATUS_TIMEOUT = int(os.getenv("ORDER_STATUS_TIMEOUT", 5))  # Таймаут проверки статуса

# Задержки между операциями
ORDER_CANCEL_DELAY = float(os.getenv("ORDER_CANCEL_DELAY", 0.5))  # Задержка при отмене ордера
ERROR_RETRY_DELAY = float(os.getenv("ERROR_RETRY_DELAY", 1.0))  # Задержка при ошибке

# Проверка обязательных параметров
if not all([API_KEY, API_SECRET]):
    raise ValueError("Необходимо указать API_KEY и API_SECRET в файле .env")
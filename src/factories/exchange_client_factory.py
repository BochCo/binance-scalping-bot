# src/factories/exchange_client_factory.py

from src.exchange.binance_futures_client import BinanceFuturesClient
from src.exchange.binance_spot_client import BinanceSpotClient
from src.exchange.bybit_futures_client import BybitFuturesClient
from src.exchange.bybit_spot_client import BybitSpotClient

def get_exchange_client(config):
    """
    Фабрика для создания клиентов бирж.

    Args:
        config (configparser.ConfigParser): Объект ConfigParser с настройками.

    Returns:
        IExchangeClient: Экземпляр клиента биржи.

    Raises:
        ValueError: Если указан неверный тип биржи или рынка.
    """
    exchange = config['DEFAULT']['exchange']
    market_type = config['DEFAULT']['market_type']
    bybit_api_key = config['DEFAULT']['bybit_api_key']
    bybit_api_secret = config['DEFAULT']['bybit_api_secret']
    binance_api_key = config['DEFAULT']['binance_api_key']
    binance_api_secret = config['DEFAULT']['binance_api_secret']

    if exchange == "bybit" and market_type == "futures":
        use_testnet = config['BYBIT'].getboolean('use_testnet')
        return BybitFuturesClient(bybit_api_key, bybit_api_secret, use_testnet)
    elif exchange == "bybit" and market_type == "spot":
        return BybitSpotClient(bybit_api_key, bybit_api_secret) # Еще не реализован
    elif exchange == "binance" and market_type == "futures":
        return BinanceFuturesClient(binance_api_key, binance_api_secret) # Еще не реализован
    elif exchange == "binance" and market_type == "spot":
        return BinanceSpotClient(binance_api_key, binance_api_secret) # Еще не реализован
    else:
        raise ValueError("Неверный тип биржи или рынка в конфигурации")
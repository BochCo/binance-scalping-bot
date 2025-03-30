# main.py

from src.utils.config_reader import read_config
from src.factories.exchange_client_factory import get_exchange_client

def main():
    """
    Основная функция для запуска бота.
    """
    try:
        config = read_config()
        client = get_exchange_client(config)

        # Пример использования Bybit Futures Testnet
        if isinstance(client, BybitFuturesClient):
            market_data = client.get_market_data("BTCUSDT")
            print(f"Данные о рынке: {market_data}")

            balance = client.get_balance("USDT")
            print(f"Баланс: {balance}")

            # result = client.place_order(symbol="BTCUSDT", side="BUY", type="MARKET", quantity=0.001)
            # print(f"Результат размещения ордера: {result}")

            # order_id = result['result']['order_id']
            # cancel_result = client.cancel_order(order_id=order_id, symbol="BTCUSDT")
            # print(f"Результат отмены ордера: {cancel_result}")

        else:
            print("Этот пример предназначен только для Bybit Futures.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
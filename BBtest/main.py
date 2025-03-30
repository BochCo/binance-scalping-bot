# main.py

from bot import Bot

def main():
    bot = Bot()
    
    try:
        # Получаем данные о рынке
        market_data = bot.get_market_data("BTCUSDT")
        print("Данные о рынке:", market_data)
        
        # Получаем баланс
        balance = bot.get_balance("USDT")
        print("Баланс:", balance)
        
        # Размещаем тестовый ордер
        order = bot.place_order(
            symbol="BTCUSDT",
            side="buy",
            order_type="limit",
            qty=0.001,
            price=25000
        )
        print("Размещённый ордер:", order)
    
    except Exception as e:
        print("Произошла ошибка:", e)

if __name__ == "__main__":
    main()
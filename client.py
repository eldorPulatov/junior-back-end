import asyncio
import time

from classes import Database, DeribitClient

async def main():
    db = Database()
    await db.init_db()

    client = DeribitClient()

    # Добавляем несколько валют для отслеживания
    currencies = ["btc", "eth", "ltc"]  # BTC, ETH и LTC

    # Получение цены
    while True:
        for currency in currencies:
            price_data = await client.fetch_price(currency)

            if price_data:
                # Сохранение цены в базу данных
                await db.save_price(price_data)
                print(f"Цена {currency}: {price_data['price']} сохранена в базе данных.")

                # Получение всех цен для проверки
                all_prices = await db.get_all_prices(currency)
                print(f"Все цены для {currency}: {all_prices}")

        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())

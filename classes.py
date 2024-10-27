import aiohttp
import aiosqlite
import asyncio
import time
from typing import Optional, List, Dict

class DeribitClient:
    BASE_URL = "https://www.deribit.com/api/v2/public/get_index_price"

    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def fetch_price(self, currency: str) -> Optional[Dict[str, float]]:
        params = {"index_name": f"{currency}_usd"}
        async with self.session.get(self.BASE_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return {
                    "ticker": currency,
                    "price": data["result"]["index_price"],
                    "timestamp": int(time.time())
                }
            return None

    async def close(self):
        await self.session.close()

class Database:
    def __init__(self, db_name: str = "prices.db"):
        self.db_name = db_name

    async def init_db(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT,
                    price REAL,
                    timestamp INTEGER
                )
            ''')
            await db.commit()

    async def save_price(self, data: Dict[str, float]):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                INSERT INTO prices (ticker, price, timestamp)
                VALUES (?, ?, ?)
            ''', (data["ticker"], data["price"], data["timestamp"]))
            await db.commit()

    async def get_all_prices(self, ticker: str) -> List[Dict[str, float]]:
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT ticker, price, timestamp FROM prices WHERE ticker = ?', (ticker,)) as cursor:
                return [{"ticker": row[0], "price": row[1], "timestamp": row[2]} for row in await cursor.fetchall()]

    async def get_latest_price(self, ticker: str) -> Optional[Dict[str, float]]:
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('''
                SELECT ticker, price, timestamp FROM prices 
                WHERE ticker = ? 
                ORDER BY timestamp DESC LIMIT 1
            ''', (ticker,)) as cursor:
                row = await cursor.fetchone()
                return {"ticker": row[0], "price": row[1], "timestamp": row[2]} if row else None

    async def get_prices_by_date(self, ticker: str, date: int) -> List[Dict[str, float]]:
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('''
                SELECT ticker, price, timestamp FROM prices 
                WHERE ticker = ? AND timestamp >= ?
            ''', (ticker, date)) as cursor:
                return [{"ticker": row[0], "price": row[1], "timestamp": row[2]} for row in await cursor.fetchall()]
from pandas import DataFrame
import asyncpg
from settings import DB_CONFIG
from datetime import date


async def add_sale(user_id: int, sale_date: date, total_sum: float, address: str, phone_number: str) -> int:
    """
    Добавляет запись о продаже в таблицу sales и возвращает идентификатор добавленной продажи.
    """
    total_sum = float(total_sum)
    query = """
        INSERT INTO sales (user_id, total_sum, sale_date, address, phone_number)
        VALUES ($1, $2, $3, $4, $5) RETURNING sale_id;
    """
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            sale_id = await conn.fetchval(query, user_id, total_sum, sale_date, address, phone_number)
            return sale_id


async def add_sale_details(sales: DataFrame) -> None:
    """
    Добавляет детали продаж в таблицу sales_details на основе DataFrame.
    """
    query = """
        INSERT INTO sales_details (sale_id, barcode, quantity, price_per_piece, total_price)
        VALUES ($1, $2, $3, $4, $5);
    """
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            # Преобразуем DataFrame в список кортежей для передачи в executemany
            records = sales[["sale_id", "barcode", "quantity", "price_per_piece", "total_price"]].to_records(index=False)
            await conn.executemany(query, records)

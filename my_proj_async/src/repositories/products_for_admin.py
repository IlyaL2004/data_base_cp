import asyncpg
from settings import DB_CONFIG
from datetime import datetime


async def check_product(barcode, name, weight):
    query_check = "SELECT COUNT(*) FROM products WHERE barcode = $1 AND name = $2 AND weight = $3;"
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            count = await conn.fetchval(query_check, barcode, name, weight)
            return count > 0


async def check_supplier(name, phone):
    query_check = "SELECT COUNT(*) FROM suppliers WHERE name = $1 AND phone = $2;"
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            count = await conn.fetchval(query_check, name, phone)
            return count > 0


async def check_category(name):
    query_check = "SELECT COUNT(*) FROM categories WHERE name = $1;"
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            count = await conn.fetchval(query_check, name)
            return count > 0


async def push_supplier(name, phone, address):
    query = """
        INSERT INTO suppliers (name, phone, address)
        VALUES ($1, $2, $3);
    """
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            await conn.execute(query, name, phone, address)


async def get_id_supplier(name):
    query = """SELECT supplier_id FROM suppliers WHERE name = $1;"""
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            result = await conn.fetchval(query, name)
            return result


async def get_id_category(name):
    query = """SELECT category_id FROM categories WHERE name = $1;"""
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            result = await conn.fetchval(query, name)
            return result


async def push_date(supplier_id, delivery_date):
    query = """
        INSERT INTO deliveries (supplier_id, delivery_date)
        VALUES ($1, $2);
    """
    delivery_date = datetime.strptime(delivery_date, '%Y-%m-%d').date()
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            await conn.execute(query, supplier_id, delivery_date)


async def push_category(name):
    query = """
        INSERT INTO categories (name)
        VALUES ($1);
    """
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            await conn.execute(query, name)


async def get_id_delivery():
    query = """SELECT MAX(delivery_id) FROM deliveries;"""
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            result = await conn.fetchval(query)
            return result


async def push_product(barcode, name, package_size, weight, category_id):
    query = """
        INSERT INTO products (barcode, name, package_size, weight, category_id)
        VALUES ($1, $2, $3, $4, $5);
    """
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            await conn.execute(query, barcode, name, package_size, weight, category_id)


async def push_delivery_contents(delivery_id, barcode, quantity):
    query = """
        INSERT INTO delivery_contents (delivery_id, barcode, quantity)
        VALUES ($1, $2, $3);
    """
    delivery_id = int(delivery_id)
    quantity = int(quantity)
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            await conn.execute(query, delivery_id, barcode, quantity)


async def push_price(barcode, start_date, price):
    query = """
        INSERT INTO prices (barcode, start_date, price)
        VALUES ($1, $2, $3);
    """
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            await conn.execute(query, barcode, start_date, price)

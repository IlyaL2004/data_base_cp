import asyncpg
from settings import DB_CONFIG


async def get_products():
    print("Получение продуктов")
    query = """
        SELECT p.name, p.barcode, pr.price
        FROM products p
        JOIN prices pr 
        ON p.barcode = pr.barcode;
    """
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            products = await conn.fetch(query)
            return [dict(record) for record in products]


async def get_products_filter(id_category):
    print("Получение продуктов фильтра")
    query = """
        SELECT p.name, p.barcode, pr.price
        FROM products p
        JOIN prices pr 
        ON p.barcode = pr.barcode
        WHERE category_id = $1;
    """
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            products = await conn.fetch(query, id_category)
            return [dict(record) for record in products]


async def get_categories() -> list[dict]:
    print("Получение категорий продуктов")
    query = "SELECT name, category_id FROM categories;"
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            categories = await conn.fetch(query)
            print(categories)
            return [dict(record) for record in categories]


async def get_count_product(barcode) -> int:
    print("Получение количества продукта по штрихкоду")
    query = """
        SELECT COALESCE(dc.quantity, 0) - COALESCE(sd.quantity, 0) AS remaining_quantity
        FROM (SELECT barcode, SUM(quantity) AS quantity FROM delivery_contents GROUP BY barcode) AS dc
        LEFT JOIN (SELECT barcode, SUM(quantity) AS quantity FROM sales_details GROUP BY barcode) AS sd
        ON dc.barcode = sd.barcode
        WHERE dc.barcode = $1;
    """
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            result = await conn.fetchval(query, barcode)
            return result if result is not None else 0

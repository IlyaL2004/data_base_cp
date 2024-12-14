import asyncpg
from settings import DB_CONFIG
from datetime import datetime


async def create_trigger_and_function():
    # SQL-запрос для создания функции триггера
    trigger_function_sql = """
    CREATE OR REPLACE FUNCTION audit_price_change() 
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO price_audit (barcode, old_price, new_price)
        VALUES (OLD.barcode, OLD.price, NEW.price);
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql; 
    """

    # SQL-запрос для создания триггера
    trigger_sql = """
    CREATE TRIGGER price_update_trigger
    AFTER UPDATE ON prices
    FOR EACH ROW
    WHEN (OLD.price IS DISTINCT FROM NEW.price)
    EXECUTE FUNCTION audit_price_change();
    """

    try:
        async with asyncpg.create_pool(**DB_CONFIG) as pool:
            async with pool.acquire() as conn:
                # Создать функцию триггера
                await conn.execute(trigger_function_sql)
                # Создать триггер
                await conn.execute(trigger_sql)
                print("Trigger and function created successfully.")
    except Exception as e:
        print(f"Error creating trigger and function: {e}")


async def update_price_product(barcode: str, start_date: str, price: float):
    query_update = "UPDATE prices SET start_date = $1, price = $2 WHERE barcode = $3;"
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    try:
        async with asyncpg.create_pool(**DB_CONFIG) as pool:
            async with pool.acquire() as conn:
                await conn.execute(query_update, start_date, price, barcode)
                print("Price updated successfully.")
    except Exception as e:
        print(f"Error updating price: {e}")

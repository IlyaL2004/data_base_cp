import asyncpg
from settings import DB_CONFIG


class ReportsRepository:

    @staticmethod
    async def get_products_report():
        """Получает полный отчет по товарам"""
        query = """
        SELECT 
            p.barcode,
            p.name as product_name,
            c.name as category_name,
            pr.price as current_price,
            COALESCE(dc.total_delivered, 0) as total_delivered,
            COALESCE(sd.total_sold, 0) as total_sold,
            COALESCE(dc.total_delivered, 0) - COALESCE(sd.total_sold, 0) as stock_balance,
            s.name as main_supplier,
            p.weight,
            p.package_size
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN prices pr ON p.barcode = pr.barcode AND pr.end_date IS NULL
        LEFT JOIN (
            SELECT barcode, SUM(quantity) as total_delivered 
            FROM delivery_contents 
            GROUP BY barcode
        ) dc ON p.barcode = dc.barcode
        LEFT JOIN (
            SELECT barcode, SUM(quantity) as total_sold 
            FROM sales_details 
            GROUP BY barcode
        ) sd ON p.barcode = sd.barcode
        LEFT JOIN (
            SELECT DISTINCT ON (dc.barcode) dc.barcode, s.name
            FROM delivery_contents dc
            JOIN deliveries d ON dc.delivery_id = d.delivery_id
            JOIN suppliers s ON d.supplier_id = s.supplier_id
            ORDER BY dc.barcode, d.delivery_date DESC
        ) s ON p.barcode = s.barcode
        ORDER BY p.name;
        """

        async with asyncpg.create_pool(**DB_CONFIG) as pool:
            async with pool.acquire() as conn:
                records = await conn.fetch(query)
                return [dict(record) for record in records]

    @staticmethod
    async def get_sales_report(start_date=None, end_date=None):
        """Получает отчет по продажам за период"""
        query = """
        SELECT 
            s.sale_id,
            s.sale_date,
            u.username as customer,
            s.total_sum,
            s.address,
            s.phone_number,
            COUNT(sd.barcode) as items_count
        FROM sales s
        LEFT JOIN users u ON s.user_id = u.user_id
        LEFT JOIN sales_details sd ON s.sale_id = sd.sale_id
        WHERE 1=1
        """

        params = []
        if start_date:
            query += " AND s.sale_date >= $1"
            params.append(start_date)
        if end_date:
            query += " AND s.sale_date <= $2"
            params.append(end_date)

        query += " GROUP BY s.sale_id, u.username ORDER BY s.sale_date DESC"

        async with asyncpg.create_pool(**DB_CONFIG) as pool:
            async with pool.acquire() as conn:
                records = await conn.fetch(query, *params)
                return [dict(record) for record in records]
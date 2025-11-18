import pandas as pd
from datetime import datetime
from repositories.reports_repository import ReportsRepository


class ReportsService:

    @staticmethod
    async def get_products_report():
        """Получает и обрабатывает отчет по товарам"""
        return await ReportsRepository.get_products_report()


    async def get_sales_report(start_date=None, end_date=None):
        """Получает и обрабатывает отчет по продажам"""
        return await ReportsRepository.get_sales_report(start_date, end_date)

    @staticmethod
    async def get_stock_analysis():
        """Анализирует остатки товаров"""
        products = await ReportsRepository.get_products_report()
        if not products:
            return None

        df = pd.DataFrame(products)

        # Анализ запасов
        low_stock = df[df['stock_balance'] <= 5]
        out_of_stock = df[df['stock_balance'] <= 0]

        # Статистика по категориям
        category_stats = df.groupby('category_name').agg({
            'product_name': 'count',
            'stock_balance': 'sum',
            'current_price': 'sum'
        }).reset_index()

        return {
            'products_df': df,
            'low_stock': low_stock,
            'out_of_stock': out_of_stock,
            'category_stats': category_stats
        }

    @staticmethod
    def calculate_metrics(df):
        """Рассчитывает метрики для отчетов"""
        if df.empty:
            return {}

        metrics = {
            'total_products': len(df),
            'total_stock': df['stock_balance'].sum() if 'stock_balance' in df.columns else None,
            'total_value': df['current_price'].sum() if 'current_price' in df.columns else None,
            'low_stock_count': len(df[df['stock_balance'] <= 5]) if 'stock_balance' in df.columns else None,
            'total_sales': df['total_sum'].sum() if 'total_sum' in df.columns else None,
            'avg_sale': df['total_sum'].mean() if 'total_sum' in df.columns else None
        }

        return metrics
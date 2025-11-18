import streamlit as st
import pandas as pd
from datetime import datetime
import io
from services.reports_service import ReportsService


def convert_df_to_csv(df):
    """Конвертирует DataFrame в CSV"""
    return df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')


def convert_df_to_excel(df):
    """Конвертирует DataFrame в Excel"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Отчет')
    return output.getvalue()


async def show_reports_page():
    st.title("Отчеты для администратора")

    # Выбор типа отчета
    report_type = st.selectbox(
        "Выберите тип отчета",
        ["Отчет по товарам", "Отчет по продажам", "Аналитика остатков"]
    )

    if report_type == "Отчет по товарам":
        await show_products_report()
    elif report_type == "Отчет по продажам":
        await show_sales_report()
    elif report_type == "Аналитика остатков":
        await show_stock_analysis()


async def show_products_report():
    st.subheader("Отчет по товарам")

    if st.button("Сформировать отчет", type="primary"):
        with st.spinner("Формирование отчета..."):
            products = await ReportsService.get_products_report()

            if products:
                df = pd.DataFrame(products)

                # Показываем таблицу
                st.dataframe(df, use_container_width=True)

                # Статистика через сервис
                metrics = ReportsService.calculate_metrics(df)

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Всего товаров", metrics['total_products'])
                with col2:
                    st.metric("Товары на складе", metrics['total_stock'])
                with col3:
                    st.metric("Общая стоимость", f"{metrics['total_value']:.2f} руб")
                with col4:
                    st.metric("Низкий запас", metrics['low_stock_count'], delta_color="inverse")

                # Выгрузка
                csv = convert_df_to_csv(df)
                st.download_button(
                    label="Скачать отчет в CSV",
                    data=csv,
                    file_name=f"products_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                )
            else:
                st.warning("Нет данных для отчета")


async def show_sales_report():
    st.subheader("Отчет по продажам")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Дата начала")
    with col2:
        end_date = st.date_input("Дата окончания")

    if st.button("Сформировать отчет по продажам", type="primary"):
        with st.spinner("Формирование отчета..."):
            sales = await ReportsService.get_sales_report(start_date, end_date)

            if sales:
                df = pd.DataFrame(sales)
                st.dataframe(df, use_container_width=True)

                # Метрики через сервис
                metrics = ReportsService.calculate_metrics(df)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Всего продаж", metrics['total_products'])
                with col2:
                    st.metric("Общая выручка", f"{metrics['total_sales']:.2f} руб")
                with col3:
                    st.metric("Средний чек", f"{metrics['avg_sale']:.2f} руб")

                # Выгрузка
                csv = convert_df_to_csv(df)
                st.download_button(
                    label="Скачать отчет в CSV",
                    data=csv,
                    file_name=f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                )


async def show_stock_analysis():
    st.subheader("Аналитика остатков товаров")

    if st.button("Сформировать анализ", type="primary"):
        with st.spinner("Формирование анализа..."):
            analysis_data = await ReportsService.get_stock_analysis()

            if analysis_data:
                # Товары с низким запасом
                low_stock = analysis_data['low_stock']
                out_of_stock = analysis_data['out_of_stock']

                st.write("### Товары с низким запасом (≤ 5 шт)")
                if not low_stock.empty:
                    st.dataframe(low_stock[['product_name', 'barcode', 'stock_balance', 'main_supplier']])
                else:
                    st.success("Нет товаров с низким запасом")

                st.write("### Отсутствующие товары")
                if not out_of_stock.empty:
                    st.dataframe(out_of_stock[['product_name', 'barcode', 'stock_balance', 'main_supplier']])
                else:
                    st.success("Нет отсутствующих товаров")

                # Статистика по категориям
                st.write("### Статистика по категориям")
                st.dataframe(analysis_data['category_stats'].rename(columns={
                    'product_name': 'Количество товаров',
                    'stock_balance': 'Остаток на складе',
                    'current_price': 'Общая стоимость'
                }))
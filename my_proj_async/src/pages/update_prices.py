import streamlit as st
from repositories.products_for_admin import check_product
from repositories.update_prices_products import update_price_product
async def update_price():
    st.title("Здесь можно обновить цену")

    barcode_product = st.text_input("Введите barcode товара")
    weight_product = st.text_input("Введите вес товара")
    name_product = st.text_input("Введите название товара")
    start_date_product = st.text_input("Введите дату установки цены (в формате YYYY-MM-DD)")
    price = st.text_input("Введите цену товара")

    update_price_button = st.button("Обновить цену товара")

    if update_price_button:
        # Проверяем, заполнены ли все поля
        if not all([barcode_product, weight_product, name_product, start_date_product, price]):
            st.error("Пожалуйста, заполните все поля.")
            return

        try:
            price = float(price)
        except ValueError:
            st.error("Цена должна быть числом.")
            return

        # Проверяем наличие товара
        product_exists = await check_product(barcode_product, name_product, weight_product)
        if product_exists:
            st.success("Такой товар есть!")
            await update_price_product(barcode_product, start_date_product, price)
            st.success("Цена товара обновлена!")
        else:
            st.error("Такого товара нет!")


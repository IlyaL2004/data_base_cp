import streamlit as st
import pandas as pd
from datetime import date
import random
from services.sales import SalesService  # Асинхронный сервис продаж
from repositories.products import get_count_product, get_products, get_products_filter, get_categories




if "sales_table" not in st.session_state:
    st.session_state.sales_table = pd.DataFrame(
        columns=["Название продукта", "Barcode", "Количество", "Цена за штуку", "Суммарная цена"]
    )

if "total_sum" not in st.session_state:
    st.session_state.total_sum = 0.0


def update_total_sum():
    """Обновление общей суммы заказа."""
    st.session_state.total_sum = st.session_state.sales_table["Суммарная цена"].sum()


async def get_everything_quantity_product(product_barcode):
    """Асинхронное получение доступного количества товара на складе."""
    return await get_count_product(product_barcode)


def get_quantity_product_from_basket(product_barcode):
    """Получение количества товара в корзине."""
    product_row = st.session_state.sales_table.loc[
        st.session_state.sales_table['Barcode'] == product_barcode
    ]
    if not product_row.empty:
        return product_row['Количество'].values[0]
    return 0


async def add_product_event(product_name, product_barcode, product_quantity, product_price):
    """Асинхронное добавление продукта в корзину."""
    everything_quantity_product = await get_everything_quantity_product(product_barcode)
    print(everything_quantity_product)
    everything_quantity_product = everything_quantity_product
    quantity_product_from_basket = get_quantity_product_from_basket(product_barcode)

    if everything_quantity_product >= product_quantity + quantity_product_from_basket:
        if any(st.session_state.sales_table['Barcode'] == product_barcode):
            st.session_state.sales_table.loc[
                st.session_state.sales_table['Barcode'] == product_barcode, 'Количество'
            ] += product_quantity
            st.session_state.sales_table.loc[
                st.session_state.sales_table['Barcode'] == product_barcode, 'Цена за штуку'
            ] = product_price
            st.session_state.sales_table.loc[
                st.session_state.sales_table['Barcode'] == product_barcode, 'Суммарная цена'
            ] = (
                st.session_state.sales_table.loc[
                    st.session_state.sales_table['Barcode'] == product_barcode, 'Количество'
                ]
                * float(product_price)
            )
            update_total_sum()
        else:
            new_row = pd.DataFrame(
                {
                    "Название продукта": [product_name],
                    "Barcode": [product_barcode],
                    "Количество": [product_quantity],
                    "Цена за штуку": [product_price],
                    "Суммарная цена": [float(product_quantity) * float(product_price)],
                }
            )
            st.session_state.sales_table = pd.concat(
                [st.session_state.sales_table, new_row], ignore_index=True
            )
            update_total_sum()
    else:
        st.error(
            f"Недостаточно товара на складе."
            f"Имеется только {everything_quantity_product} из {product_quantity + quantity_product_from_basket} требуемых."
        )


async def upload_sales(sales_table, total_sum, address, phone_number):
    """Асинхронная загрузка продажи."""
    sale_date = date(2024, random.randint(1, 12), random.randint(1, 28))
    sale_id = await SalesService().process_sale(
        sale_date, sales_table, total_sum, address, phone_number
    )
    st.write(f"Продажа за число {sale_date}")
    return sale_id


def clear_table_event():
    """Очистка корзины."""
    st.session_state.sales_table = pd.DataFrame(
        columns=["Название продукта", "Barcode", "Количество", "Цена за штуку", "Суммарная цена"]
    )
    update_total_sum()


async def show_selling_products_page():
    st.title("Продажа продуктов")

    categories = await get_categories()
    print(categories)#
    category_dict = {category['name']: category['category_id'] for category in categories}
    selected_category = st.selectbox("Выберите категорию", category_dict.keys())
    add_filter_btn = st.button("Применить фильтр")

    if add_filter_btn and category_dict[selected_category] != 0:
        products = await get_products_filter(category_dict[selected_category])
    elif category_dict[selected_category] != 0:
        print(1111)
        print(selected_category)
        products = await get_products_filter(category_dict[selected_category])
    else:
        products = await get_products()
        print(products)
    options = [
        f"{product['name']} | Штрих-код: | {product['barcode']} | Цена за штуку: | {product['price']} | руб."
        for product in products
    ]


    selected_product = st.selectbox("Выберите продукт", options)
    selected_name = selected_product.split(" | ")[0]
    selected_barcode = selected_product.split(" | ")[2]
    selected_price = selected_product.split(" | ")[4]

    quantity = st.number_input("Количество", min_value=1, max_value=100, value=1)
    add_product_btn = st.button("Добавить продукт")

    if add_product_btn:
        await add_product_event(selected_name, selected_barcode, quantity, selected_price)

    clear_table_btn = st.button("Очистить корзину")
    apply_btn = st.button("Сделать заказ")
    address = st.text_input("Введите адрес доставки")
    phone_number = st.text_input("Введите номер телефона")

    if clear_table_btn:
        clear_table_event()

    if apply_btn and len(st.session_state.sales_table) > 0:
        if not address or not phone_number:
            st.warning("Все поля обязательны для заполнения.")
            return

        for index, row in st.session_state.sales_table.iterrows():
            name = row["Название продукта"]
            barcode = row["Barcode"]
            quantity = row["Количество"]
            quantity_warehouse = await get_everything_quantity_product(barcode)
            quantity_warehouse = quantity_warehouse

            if quantity_warehouse < quantity:
                st.error(
                    f"Недостаточно {name} на складе. "
                    f"Пока вы выбирали, осталось только {quantity_warehouse}."
                )
                return

        sale_id = await upload_sales(
            st.session_state.sales_table, st.session_state.total_sum, address, phone_number
        )
        st.success(f"Продажа добавлена успешно! ID чека: {sale_id}")
        clear_table_event()
        update_total_sum()

    st.write("Добавленные товары:")
    st.dataframe(st.session_state.sales_table)
    st.write(f"**Сумма всего заказа:** {st.session_state.total_sum:.2f}")



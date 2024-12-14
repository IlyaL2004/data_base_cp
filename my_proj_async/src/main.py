from pages.selling_products import show_selling_products_page
import streamlit as st
from pages.login import login, check_role
from pages.register import show_register_page  # Новая страница регистрации
from pages.user_management import user_rights, add_user_or_admin
from pages.add_products import add_products_admin
from pages.update_prices import update_price
from repositories.update_prices_products import create_trigger_and_function
import asyncio
import pandas as pd
# Обертка для вызова асинхронных функций в синхронном контексте Streamlit
def run_async_function(async_func, *args, **kwargs):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(async_func(*args, **kwargs))
    loop.close()
    return result


# Асинхронная версия create_trigger_and_function
async def async_create_trigger_and_function():
    await create_trigger_and_function()


# Асинхронная логика главной функции
async def main_async():
    try:
        st.sidebar.title("Навигация")

    # Асинхронное создание триггера и функции
        await async_create_trigger_and_function()

        if "auth_token" not in st.session_state:
            page = st.sidebar.radio(
                "Выберите действие", ["Вход", "Регистрация"]
            )
            if page == "Вход":
                await login()
            elif page == "Регистрация":
                await show_register_page()
        else:
            if await check_role("user"):
                page = st.sidebar.radio(
                    "Перейти к странице",
                    ["Сделать заказ", "Выйти"],
                )
                if page == "Сделать заказ":
                    if "sales_table" not in st.session_state:
                        st.session_state.sales_table = pd.DataFrame(
                            columns=["Название продукта", "Barcode", "Количество", "Цена за штуку", "Суммарная цена"]
                        )

                    if "total_sum" not in st.session_state:
                        st.session_state.total_sum = 0.0
                    try:

                        await show_selling_products_page()
                    except Exception as e:
                        st.text(f"Internal server error: {e}")

                elif page == "Выйти":
                    exit_from_page = st.button("Выйти")
                    if exit_from_page:
                        st.session_state.pop("auth_token", None)
                        st.success("Вы вышли из системы")
            elif await check_role("admin"):
                page = st.sidebar.radio(
                    "Перейти к странице",
                    [
                        "Сделать заказ",
                        "Управление пользовательскими правами",
                        "Добавить пользователя или админа",
                        "Добавить товар, категорию, поставщика",
                        "Обновить цену",
                        "Выйти",
                    ],
                )
                if page == "Сделать заказ":
                    await show_selling_products_page()
                elif page == "Управление пользовательскими правами":
                    await user_rights()
                elif page == "Добавить пользователя или админа":
                    await add_user_or_admin()
                elif page == "Добавить товар, категорию, поставщика":
                    await add_products_admin()
                elif page == "Обновить цену":
                    await update_price()
                elif page == "Выйти":
                    exit_from_page = st.button("Выйти")
                    if exit_from_page:
                        st.session_state.pop("auth_token", None)
                        st.success("Вы вышли из системы")
    except Exception as e:
        st.text(f"Internal server error: {e}")

# Главная логика приложения
def main():
    run_async_function(main_async)


if __name__ == "__main__":
    main()

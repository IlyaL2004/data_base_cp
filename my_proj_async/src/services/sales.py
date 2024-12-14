from datetime import datetime
from pandas import DataFrame
import jwt
from jwt import DecodeError, ExpiredSignatureError
import streamlit as st

# Импорт асинхронных функций
from repositories.sales import add_sale, add_sale_details  # Предполагается, что они асинхронные


class SalesService:
    async def process_sale(self, sale_date: datetime, items: DataFrame, total_sum, address, phone_number) -> int:
        """
        Обработка продажи: сохраняет данные о продаже и деталях продажи.
        """
        # Переименовываем колонки DataFrame для базы данных
        items = items.rename(
            columns={
                "Количество": "quantity",
                "Barcode": "barcode",
                "Цена за штуку": "price_per_piece",
                "Суммарная цена": "total_price",
            }
        )

        SECRET_KEY = "your_secret_key"
        token = st.session_state.get("auth_token")

        if not token:
            st.error("Вы не авторизованы")
            return False

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload["user_id"]
        except (DecodeError, ExpiredSignatureError):
            st.error("Невалидный или просроченный токен")
            return False

        # Асинхронное добавление продажи
        sale_id = await add_sale(user_id, sale_date, total_sum, address, phone_number)

        # Добавление ID продажи в DataFrame
        items["sale_id"] = sale_id

        # Асинхронное добавление деталей продажи
        await add_sale_details(items)

        return sale_id

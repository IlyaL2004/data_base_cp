import streamlit as st
import re
import asyncio
from repositories.users import add_user, restrict_rights


async def user_rights():
    st.title("Выберите пользователя, которому вы хотите ограничить права доступа или восстановить права")
    username = st.text_input("Введите имя пользователя")
    right_button = st.selectbox(
        "Выберите TRUE, если вы хотите восстановить права, или FALSE, если вы хотите ограничить права",
        ["TRUE", "FALSE"]
    )
    button_apply = st.button("Применить изменения")
    if button_apply:
        right_value = True if right_button == "TRUE" else False
        right_change = await restrict_rights(right_value, username)
        if right_change:
            st.success("Пользовательские права были изменены!")
        else:
            st.error("Пользователя с таким именем не существует!")


async def add_user_or_admin():
    st.title("Добавить пользователя или администратора")

    with st.form("register_form"):
        username = st.text_input("Введите логин")
        password = st.text_input("Введите пароль", type="password")
        confirm_password = st.text_input("Повторите пароль", type="password")
        role = st.selectbox("Выберите роль", ["user", "admin"])
        email = st.text_input("Введите адрес электронной почты")
        submit_button = st.form_submit_button("Зарегистрировать")

        if submit_button:
            # Проверка валидности данных
            if not username or not password or not confirm_password or not role or not email:
                st.warning("Все поля обязательны для заполнения.")
                return

            if not re.match(r"^[a-zA-Z0-9_]+$", username):
                st.error("Имя пользователя может содержать только буквы, цифры и _.")
                return

            if len(password) < 6:
                st.error("Пароль должен быть длиной не менее 6 символов.")
                return

            if password != confirm_password:
                st.error("Пароли не совпадают.")
                return

            # Асинхронное добавление пользователя
            try:
                await add_user(username, password, role, email, active=True)
                st.success(f"Пользователь {username} успешно зарегистрирован!")
            except ValueError as e:
                st.error(str(e))


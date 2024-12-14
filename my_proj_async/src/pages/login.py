import streamlit as st
import jwt
from jwt import DecodeError, ExpiredSignatureError
from services.auth import authenticate_user, active_user

SECRET_KEY = "your_secret_key"

async def login():
    st.title("Вход")

    username = st.text_input("Логин")
    password = st.text_input("Пароль", type="password")
    login_button = st.button("Войти")

    if login_button:
        # Асинхронная проверка пользователя
        rez = await active_user(username)
        if rez:
            token = await authenticate_user(username, password)
            if token:
                st.session_state["auth_token"] = token
                st.success("Вход выполнен!")
            else:
                st.error("Неверный логин или пароль")
        elif rez is None:
            st.error("Пользователя c таким именем не существует!")
        else:
            st.error("Пользователь с таким именем заблокирован!")

async def check_role(required_role: str) -> bool:
    token = st.session_state.get("auth_token")
    if not token:
        st.error("Вы не авторизованы")
        return False

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if payload["role"] != required_role:
            return False
        return True
    except (DecodeError, ExpiredSignatureError):
        st.error("Невалидный или просроченный токен")
        return False


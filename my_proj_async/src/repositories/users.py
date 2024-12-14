from services.auth import hash_password
import asyncpg
from settings import DB_CONFIG


async def add_user(username: str, password: str, role: str = "user", email: str = "non@yandex.ru", active: bool = True):
    query_check = "SELECT COUNT(*) FROM users WHERE username = $1;"
    query_email = "SELECT COUNT(*) FROM users WHERE email = $1;"
    query_insert = "INSERT INTO users (username, password_hash, role, email, active) VALUES ($1, $2, $3, $4, $5);"

    # Подключение к базе данных
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            # Проверка, существует ли пользователь
            count = await conn.fetchval(query_check, username)
            if count > 0:
                raise ValueError("Пользователь с таким логином уже существует.")
            count = await conn.fetchval(query_email, email)
            if count > 0:
                raise ValueError("Пользователь с такой электронной почтой существует.")

            # Хеширование пароля
            password_hash = hash_password(password)

            # Сохранение пользователя
            await conn.execute(query_insert, username, password_hash, role, email, active)


async def restrict_rights(right: bool, username: str):
    query_check = "SELECT COUNT(*) FROM users WHERE username = $1;"
    query_update = "UPDATE users SET active = $1 WHERE username = $2;"

    # Подключение к базе данных
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            # Проверка, существует ли пользователь
            count = await conn.fetchval(query_check, username)
            if count == 0:
                return False

            # Обновление прав
            await conn.execute(query_update, right, username)
            return True


import bcrypt
import jwt
import datetime
import asyncpg
from settings import DB_CONFIG

# Секретный ключ для подписания JWT
SECRET_KEY = "your_secret_key"  # Замените на ваш собственный ключ

# --- Функции для работы с паролями ---
def hash_password(password: str) -> str:
    """
    Хеширует пароль с использованием bcrypt.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """
    Проверяет соответствие пароля и хеша.
    """
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


# --- Функции для работы с JWT ---
def generate_jwt(user_id: int, role: str) -> str:
    """
    Генерирует JWT-токен с данными пользователя.
    """
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Срок действия токена - 1 час
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_jwt(token: str) -> dict:
    """
    Расшифровывает JWT-токен и возвращает полезную нагрузку.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])


# --- Асинхронная функция для аутентификации ---
async def authenticate_user(username: str, password: str):
    """
    Аутентифицирует пользователя по имени и паролю.
    Возвращает JWT-токен, если аутентификация успешна, иначе None.
    """
    query = "SELECT user_id, password_hash, role FROM users WHERE username = $1;"
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            user = await conn.fetchrow(query, username)
            if user:
                user_id, password_hash, role = user["user_id"], user["password_hash"], user["role"]
                if verify_password(password, password_hash):
                    return generate_jwt(user_id, role)
    return None


# --- Асинхронная функция проверки активности пользователя ---
async def active_user(username: str):
    """
    Проверяет активность пользователя.
    Возвращает статус активности (True/False), если пользователь существует;
    иначе возвращает None.
    """
    query = "SELECT active FROM users WHERE username = $1;"
    async with asyncpg.create_pool(**DB_CONFIG) as pool:
        async with pool.acquire() as conn:
            result = await conn.fetchval(query, username)
            return result  # Возвращает True/False или None, если пользователь не найден

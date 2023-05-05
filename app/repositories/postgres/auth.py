from app.config import config
from app.domain.user import User

import asyncpg

async def create_user(user: User) -> None:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    query = """
        INSERT INTO users (username, email, password, salt) VALUES
        ($1, $2, $3, $4)
    """
    await conn.execute(query, user.username, user.email, user.password, user.salt)
    await conn.close()

async def get_user_by_username(username: str) -> User:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    query = """
        SELECT * from users WHERE username = $1
    """
    user = await conn.fetchrow(query, username)
    await conn.close()
    return user

async def get_user_by_username_and_email(username: str, email: str) -> asyncpg.Record:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    query = """
        SELECT * from users WHERE username = $1 or email = $2
    """
    user = await conn.fetchrow(query, username, email)
    await conn.close()
    return user

async def get_user_by_phone_number(phone_number: str) -> asyncpg.Record:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    query = """
        SELECT phone_number from users WHERE phone_number = $1
    """

    user = await conn.fetchrow(query, phone_number)
    await conn.close()
    return user

async def check_user_password(user_id: int):
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    query = """
        SELECT password, salt from users where id = $1
    """

    user = await conn.fetchrow(query, user_id)
    await conn.close()

    return user
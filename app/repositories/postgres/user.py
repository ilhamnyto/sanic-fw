from app.config import config
from app.domain.user import User
from typing import List
from datetime import datetime

import asyncpg

async def get_all_users(cursor: int) -> List[asyncpg.Record]:
    conn = await asyncpg.connect(config.POSTGRES_DSN)

    query = """
        SELECT username, email, date_trunc('second', created_at) as created_at FROM users
    """
    if cursor:
        query += f" WHERE date_trunc('second', created_at) > '{cursor}'"

    query += " limit 6"
    users = await conn.fetch(query)

    await conn.close()
    return users

async def get_user_by_username(username: str) -> User:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    query = """
        SELECT username, email, date_trunc('second', created_at) as created_at FROM users where username = $1
    """
    user = await conn.fetchrow(query, username)
    await conn.close()
    return user

async def get_my_profile(user_id: int) -> asyncpg.Record:
    conn = await asyncpg.connect(config.POSTGRES_DSN)

    query = """
        SELECT username, email, date_trunc('second', created_at) as created_at FROM users where id = $1
        """
    user = await conn.fetchrow(query, user_id)

    await conn.close()
    return user

async def search_users(search_query: str, cursor: str) -> List[asyncpg.Record]:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    search_query = f"%{search_query}%"

    query = """
        SELECT username, email, date_trunc('second', created_at) as created_at FROM users WHERE
    """
    if cursor:
        query += f" date_trunc('second', created_at) > '{cursor}' and"

    query += ' (username like $1 or email like $1) limit 6'
    
    users = await conn.fetch(query, search_query)

    await conn.close()
    return users

async def update_user(user: User, user_id: int) -> None:
    conn = await asyncpg.connect(config.POSTGRES_DSN)

    query = """
        UPDATE users SET
        first_name = $1,
        last_name = $2,
        phone_number = $3,
        location = $4,
        updated_at = $5
        where id = $6
    """

    await conn.execute(query, user.first_name, user.last_name, user.phone_number, user.location, user.updated_at, user_id)
    await conn.close()

async def update_password(password: str, salt: str, user_id: int) -> None:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    updated_at = datetime.now()

    query = """
        UPDATE users
        SET password = $1, 
        salt = $2,
        updated_at = $3
        where id = $4
    """

    await conn.execute(query, password, salt, updated_at, user_id)
    await conn.close()



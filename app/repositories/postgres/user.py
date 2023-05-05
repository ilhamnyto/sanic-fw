from app.config import config
from app.domain.user import User
from typing import List

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




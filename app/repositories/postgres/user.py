from app.config import config
from app.domain.user import User
from typing import List

import asyncpg

async def get_all_users(page_num: int, limit: int) -> List[asyncpg.Record]:
    conn = await asyncpg.connect(config.POSTGRES_DSN)

    page_num = (page_num - 1) * limit
    query = """
        SELECT username, email, created_at FROM users WHERE id > $1 ORDER BY id ASC LIMIT $2 
    """
    users = await conn.fetch(query, page_num, limit)

    await conn.close()
    return users

async def get_my_profile(user_id: int) -> asyncpg.Record:
    conn = await asyncpg.connect(config.POSTGRES_DSN)

    query = """
        SELECT username, email, created_at FROM users WHERE id = $1
        """
    user = await conn.fetchrow(query, user_id)

    await conn.close()
    return user

async def search_users(search_query: str, cursor: str) -> List[asyncpg.Record]:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    search_query = f"%{search_query}%"

    query = """
        SELECT username, email, created_at FROM users WHERE username like $1 or email like $1
    """

    if cursor:
        query += f" and created_at > '{cursor}'"

    query += ' limit 5'
    
    users = await conn.fetch(query, search_query)

    await conn.close()
    return users




from app.config import config
from app.domain.user import User
from typing import List

import asyncpg

async def get_all_users(page_num: int, limit: int) -> List[asyncpg.Record]:
    conn = await asyncpg.connect(config.POSTGRES_DSN)

    page_num = (page_num - 1) * limit
    query = """
        SELECT * FROM users WHERE id > $1 LIMIT $2 ORDER BY id ASC
    """
    users = await conn.fetch(query, page_num, limit)

    await conn.close()
    return users

async def search_users(search_query: str, page_num: int, limit: int) -> List[asyncpg.Record]:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    search_query = f"%{search_query}%"

    page_num = (page_num - 1 )* limit
    query = """
        SELECT * FROM users WHERE username like $1 or email like $1 OFFSET $2 LIMIT $3
    """

    users = await conn.fetch(query, search_query, page_num, limit)

    await conn.close()
    return users




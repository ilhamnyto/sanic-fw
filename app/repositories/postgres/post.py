from app.domain.post import Post
from typing import List
from app.config import config
from datetime import datetime
from typing import Optional

import asyncpg

async def get_all_posts(limit: int, cursor: Optional[int] = None) -> List[asyncpg.Record]:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    query = """
        SELECT p.id, u.id, u.username, p.body, p.created_at from posts as p LEFT JOIN
        users as u ON p.user_id = u.id
    """
    if cursor is not None:
        cursor = datetime.fromtimestamp(cursor)
        query += " WHERE created_at > {cursor}"
    
    query += " LIMIT $1"
    posts = await conn.fetch(query, limit)
    await conn.close()
    return posts

async def create_posts(post: Post) -> None:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    query = """
        INSERT INTO posts (user_id, body, created_at) VALUES
        ($1, $2, $3)
    """
    await conn.execute(query, post.user_id, post.body, post.created_at)
    await conn.close()

async def get_user_posts(username: str) -> List[asyncpg.Record]:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    query = """
        SELECT p.id, u.username, p.body, p.created_at from posts as p LEFT JOIN
        users as u ON p.user_id = u.id WHERE u.username = $1
    """
    posts = await conn.fetch(query, username)
    await conn.close()
    return posts

async def get_single_post(post_id: int) -> asyncpg.Record:
    conn = asyncpg.connect(config.POSTGRES_DSN)
    query = """
        SELECT p.id, u.username, p.body, p.created_at from posts as p LEFT JOIN
        users as u ON p.user_id = u.id WHERE p.id = $1 
    """
    post = await conn.fetchrow(query, post_id)
    await conn.close()
    return post

async def search_post(query_str: str) -> List[asyncpg.Record]:
    conn = asyncpg.connect(config.POSTGRES_DSN)
    query = """
        SELECT p.id, u.username, p.body, p.created_at from posts as p LEFT JOIN
        users as u ON p.user_id = u.id WHERE u.username = $1 or p.body LIKE $2
    """
    posts = await conn.fetch(query)
    await conn.close()
    return posts
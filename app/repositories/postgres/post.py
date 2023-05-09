from app.domain.post import Post
from typing import List
from app.config import config
from datetime import datetime
from typing import Optional

import asyncpg

async def get_all_posts(cursor: Optional[datetime] = None) -> List[asyncpg.Record]:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    query = """
        SELECT p.id as posts_id, u.username, p.body, date_trunc('second', p.created_at) as created_at from posts as p LEFT JOIN
        users as u ON p.user_id = u.id
    """
    if cursor:
        query += f" WHERE date_trunc('second', p.created_at) > '{cursor}'"
    query += " ORDER BY p.created_at DESC LIMIT 6"
    posts = await conn.fetch(query)
    await conn.close()
    return posts

async def get_my_posts(user_id: int, cursor: Optional[int] = None) -> List[asyncpg.Record]:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    query = """
        SELECT p.id as posts_id, u.username, p.body, date_trunc('second', p.created_at) as created_at from posts as p LEFT JOIN
        users as u ON p.user_id = u.id WHERE u.id = $1
    """
    if cursor:
        query += f" and date_trunc('second', p.created_at) < '{cursor}'"
    
    query += " ORDER BY p.created_at DESC LIMIT 6"
    posts = await conn.fetch(query, user_id)
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

async def get_user_posts(username: str, cursor: Optional[int] = None) -> List[asyncpg.Record]:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    query = """
        SELECT p.id as posts_id, u.username, p.body, date_trunc('second', p.created_at) as created_at from posts as p LEFT JOIN
        users as u ON p.user_id = u.id WHERE u.username = $1
    """
    if cursor:
        query += f" AND date_trunc('second', p.created_at) < '{cursor}'"

    query += " ORDER BY p.created_at DESC LIMIT 6"

    posts = await conn.fetch(query, username)
    await conn.close()
    return posts

async def get_single_post(post_id: int) -> asyncpg.Record:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    query = """
        SELECT p.id as posts_id, u.username, p.body, p.created_at from posts as p LEFT JOIN
        users as u ON p.user_id = u.id WHERE p.id = $1 
    """
    post = await conn.fetchrow(query, post_id)
    await conn.close()
    return post

async def search_post(search_query: str, cursor: Optional[int] = None) -> List[asyncpg.Record]:
    conn = await asyncpg.connect(config.POSTGRES_DSN)

    search_query = f"%{search_query}%"

    query = """
        SELECT p.id as posts_id, u.username, p.body, p.created_at from posts as p LEFT JOIN
        users as u ON p.user_id = u.id WHERE 
    """

    if cursor:
        query += f" date_trunc('second', p.created_at) < '{cursor}' and"

    query += " (u.username LIKE $1 or p.body LIKE $1) ORDER BY p.created_at DESC LIMIT 6"

    posts = await conn.fetch(query, search_query)
    await conn.close()
    return posts
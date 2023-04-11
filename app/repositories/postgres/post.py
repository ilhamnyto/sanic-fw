from app.domain.post import Post
from typing import List
from app.config import config
from datetime import datetime
from typing import Optional

import asyncpg

async def get_all_posts(limit: int, cursor: Optional[int] = None) -> List[asyncpg.Record]:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    query = """
        SELECT p.id as posts_id, u.id as user_id, u.username, p.body, p.created_at from posts as p LEFT JOIN
        users as u ON p.user_id = u.id ORDER BY created_at DESC
    """
    if cursor is not None:
        cursor = datetime.fromtimestamp(cursor)
        query += " WHERE created_at > {cursor}"
    
    query += " LIMIT $1"
    posts = await conn.fetch(query, limit)
    await conn.close()
    return posts

async def get_my_posts(user_id: int, limit: int, cursor: Optional[int] = None) -> List[asyncpg.Record]:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    query = """
        SELECT p.id as posts_id, u.id as user_id, u.username, p.body, p.created_at from posts as p LEFT JOIN
        users as u ON p.user_id = u.id WHERE u.id = $1
    """
    if cursor is not None:
        cursor = datetime.fromtimestamp(cursor)
        query += " AND created_at > {cursor}"
    
    query += " ORDER BY created_at DESC LIMIT $2"
    posts = await conn.fetch(query, user_id, limit)
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
        SELECT p.id as posts_id, u.username, p.body, p.created_at from posts as p LEFT JOIN
        users as u ON p.user_id = u.id WHERE u.username = $1 ORDER BY created_at DESC
    """
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

async def search_post(search_query: str) -> List[asyncpg.Record]:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    search_query = f"%{search_query}%"
    query = """
        SELECT p.id as posts_id, u.username, p.body, p.created_at from posts as p LEFT JOIN
        users as u ON p.user_id = u.id WHERE u.username LIKE $1 or p.body LIKE $1 ORDER BY created_at DESC
    """
    posts = await conn.fetch(query, search_query)
    await conn.close()
    return posts
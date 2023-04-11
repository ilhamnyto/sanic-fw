import base64
from app.domain.post import Post, PostData
from app.repositories.postgres.post import get_all_posts, get_single_post, get_user_posts, create_posts, search_post
from typing import Optional
from datetime import datetime

async def all_posts_services(limit: int, cursor: Optional[int] = None) -> None:
    resp = await get_all_posts(limit, cursor)
    if not resp:
        return None
    posts = [ PostData(
        posts_id=base64.b64encode(f'{post["posts_id"]}:{post["username"]}'.encode('utf-8')).decode('utf-8'),
        username=post["username"],
        body=post["body"], created_at=post["created_at"].strftime("%Y-%m-%d"),
        ) for post in resp]
    return posts

async def create_posts_services(data: dict) -> None:
    post = Post(**data, user_id=2, created_at=datetime.now())
    await create_posts(post)

async def get_user_posts_services(username: str) -> None:
    resp = await get_user_posts(username)
    if not resp:
        return None
    posts = [ PostData(
        posts_id=base64.b64encode(f'{post["posts_id"]}:{post["username"]}'.encode('utf-8')).decode('utf-8'),
        username=post["username"],
        body=post["body"], created_at=post["created_at"].strftime("%Y-%m-%d"),
        ) for post in resp]
    return posts

async def get_single_post_services(post_id: str) -> None:
    try:
        post_id = base64.b64decode(post_id.encode('utf-8')).decode('utf-8').split(':')
        resp = await get_single_post(int(post_id[0]))
    except:
        return None
    if not resp:
        return None
    posts = PostData(
        posts_id=base64.b64encode(f'{resp["posts_id"]}:{resp["username"]}'.encode('utf-8')).decode('utf-8'),
        username=resp["username"],
        body=resp["body"], created_at=resp["created_at"].strftime("%Y-%m-%d"))
    return posts
    

async def search_post_services(search_query: str) -> None:
    resp = await search_post(search_query)
    if not resp:
        return None
    posts = [ PostData(
        posts_id=base64.b64encode(f'{post["posts_id"]}:{post["username"]}'.encode('utf-8')).decode('utf-8'),
        username=post["username"],
        body=post["body"], created_at=post["created_at"].strftime("%Y-%m-%d"),
        ) for post in resp]
    return posts
    
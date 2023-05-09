import base64
from app.domain.post import Post, PostData
from app.repositories.postgres.post import get_all_posts, get_single_post, get_user_posts, create_posts, search_post, get_my_posts
from typing import Optional
from datetime import datetime

async def all_posts_services(cursor: Optional[int] = None) -> None:
    if cursor:
        cursor = datetime.fromtimestamp(cursor)
    resp = await get_all_posts(cursor)
    if not resp:
        return None, False
    posts = [ PostData(
        posts_id=base64.b64encode(f'{post["posts_id"]}:{post["username"]}'.encode('utf-8')).decode('utf-8'),
        username=post["username"],
        body=post["body"], created_at=post['created_at'],
        ) for post in resp[:5]]
    
    next = len(list(resp)) > 5
    return posts, next

async def my_posts_services(user_id: int, cursor: Optional[int] = None) -> None:
    if cursor:
        cursor = datetime.fromtimestamp(cursor)

    resp = await get_my_posts(user_id, cursor)

    if not resp:
        return None, False
    
    posts = [ PostData(
        posts_id=base64.b64encode(f'{post["posts_id"]}:{post["username"]}'.encode('utf-8')).decode('utf-8'),
        username=post["username"],
        body=post["body"], created_at=post["created_at"],
        ) for post in resp[:5]]
    
    next = len(list(resp)) > 5
    return posts, next

async def create_posts_services(data: dict) -> None:
    post = Post(**data, created_at=datetime.now())
    await create_posts(post)

async def get_user_posts_services(username: str, cursor: Optional[int] = None) -> None:
    if cursor:
        cursor = datetime.fromtimestamp(cursor)

    resp = await get_user_posts(username, cursor)

    if not resp:
        return None, False
    
    posts = [ PostData(
        posts_id=base64.b64encode(f'{post["posts_id"]}:{post["username"]}'.encode('utf-8')).decode('utf-8'),
        username=post["username"],
        body=post["body"], created_at=post["created_at"],
        ) for post in resp[:5]]
    
    next = len(list(resp)) > 5

    return posts, next

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
    

async def search_post_services(search_query: str, cursor: Optional[int] = None) -> None:
    if cursor:
        cursor = datetime.fromtimestamp(cursor)
    resp = await search_post(search_query, cursor)

    if not resp:
        return None, False
    
    posts = [ PostData(
        posts_id=base64.b64encode(f'{post["posts_id"]}:{post["username"]}'.encode('utf-8')).decode('utf-8'),
        username=post["username"],
        body=post["body"], created_at=post["created_at"],
        ) for post in resp[:5]]
    
    next = len(list(resp)) > 5

    return posts, next
    
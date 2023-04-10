import base64
from app.domain.post import Post
from app.repositories.postgres.post import get_all_posts, get_single_post, get_user_posts, create_posts
from typing import Optional

async def all_posts_services(limit: int, cursor: Optional[int] = None) -> None:
    resp = await get_all_posts(limit, cursor)
    if not resp:
        return None
    print(list(resp))
    return None
    # posts = [ Post(id=, body=post.body, post.created_at) for post in resp]

async def create_posts_services(data: dict) -> None:
    pass

async def get_user_posts_services(username: str) -> None:
    pass

async def get_single_post_services(post_id: str) -> None:
    pass

async def search_post_services(query: str) -> None:
    pass
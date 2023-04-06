import base64
from app.domain.post import Post
from app.repositories.postgres.post import get_all_posts, get_single_post, get_user_posts, create_posts

async def all_posts_services(page_num: int, limit: int) -> None:
    pass

async def create_posts_services(data: dict) -> None:
    pass

async def get_user_posts_services(username: str) -> None:
    pass

async def get_single_post_services(post_id: str) -> None:
    pass

async def search_post_services(query: str) -> None:
    pass
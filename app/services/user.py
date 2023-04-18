from app.repositories.postgres.auth import get_user_by_username
from app.repositories.postgres.user import get_all_users, search_users, get_my_profile
from app.domain.user import User
from typing import List

async def all_users_services(page_num: int, limit: int) -> List[User]:
    resp = await get_all_users(page_num, limit)
    if not resp:
        return None
    
    users = [ User(**user) for user in resp]
    return users

async def my_profile_services(user_id: int) -> User:
    resp = await get_my_profile(user_id)
    if not resp:
        return None
    
    users = User(**resp)
    return users

async def get_users_services(username: str) -> User:
    resp = await get_user_by_username(username)
    if not resp:
        return None
    
    return User(**resp)

async def search_users_services(search_query: str, page_num: int, limit: int) -> List[User]:
    resp = await search_users(search_query, page_num, limit)

    if not resp:
        return None
    
    users = [ User(**user) for user in resp ]

    return users

async def update_profile_services() -> None:
    pass
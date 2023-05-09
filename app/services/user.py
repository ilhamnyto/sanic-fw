from datetime import datetime
from typing import Tuple

from app.repositories.postgres.user import get_all_users, search_users, get_my_profile, get_user_by_username, update_user, update_password
from app.domain.user import User
from app.utils.auth import generate_salt, hash_password
from typing import List

async def all_users_services(cursor: int) -> Tuple[List[User], bool]:
    if cursor:
        cursor = datetime.fromtimestamp(cursor)
    resp = await get_all_users(cursor)
    if not resp:
        return None, False
    
    users = [ User(username=user['username'], email=user['email'], password=None, salt=None, created_at=user['created_at']) for user in resp[:5]]
    next = len(list(resp)) > 5

    return users, next

async def my_profile_services(user_id: int) -> User:
    resp = await get_my_profile(user_id)
    if not resp:
        return None
    
    user = User(username=resp['username'], email=resp['email'], password=None, salt=None, created_at=resp['created_at'])
    return user

async def get_users_services(username: str) -> User:
    resp = await get_user_by_username(username)
    if not resp:
        return None
    
    return User(username=resp['username'], email=resp['email'], password=None, salt=None, created_at=resp['created_at'])

async def search_users_services(search_query: int, cursor: str) -> Tuple[List[User], bool]:
    if cursor:
        cursor = datetime.fromtimestamp(cursor)
    resp = await search_users(search_query, cursor)

    if not resp:
        return None, False
    
    users = [ User(username=user['username'], email=user['email'], password=None, salt=None, created_at=user['created_at']) for user in resp[:5] ]
    next = len(list(resp)) > 5

    return users, next

async def update_profile_services(data: dict, user_id: int) -> None:

    user = User(
        username=None,
        email=None,
        password=None,
        salt=None,
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        phone_number=data.get('phone_number'),
        location=data.get('location'),
        updated_at=datetime.now()
    )

    await update_user(user, user_id)

async def update_password_services(data: dict, user_id: int) -> None:
    salt = await generate_salt()
    hashed_password = await hash_password(salt=salt, password=data.get('password'))

    await update_password(hashed_password, salt, user_id)
from app.domain.user import User
from app.utils.auth import generate_salt, validate_password, hash_password
from app.repositories.postgres.auth import create_user, get_user_by_username

async def register_services(data: dict) -> None:
    salt = await generate_salt()
    hashed_password = await hash_password(salt=salt, password=data.get('password'))
    user = User(
        username=data.get('username'),
        email=data.get('email'),
        password=hashed_password,
        salt=salt
    )
    await create_user(user)

async def login_services(data: dict) -> User:
    resp = await get_user_by_username(data.get('username'))
    if not resp:
        return None

    user = User(**resp)
    validated_user = await validate_password(user, data.get('password'))

    if not validated_user:
        return None

    return user


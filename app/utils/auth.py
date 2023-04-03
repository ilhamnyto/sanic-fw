import secrets
import hashlib
from app.domain.user import User
from app.repositories.postgres.auth import get_user_by_username_and_email

async def validate_user_register_data(data: bool) -> bool:
    if not data.get('username') or not data.get('password') or not '@' in data.get('email'):
        return False
    elif len(data.get('username')) < 6 or len(data.get('password')) < 8 or not data.get('email'):
        return False
    
    user = await get_user_by_username_and_email(data.get('username'), data.get('email'))
    print(user)
    if user:
        return False

    return True

async def generate_salt() -> str:
    return secrets.token_hex(32)

async def hash_password(salt: str, password: str) -> str:
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt), 100000).hex()

async def validate_password(user: User, password: str) -> bool:
    expected_password = await hash_password(user.salt, password)

    return user.password == expected_password

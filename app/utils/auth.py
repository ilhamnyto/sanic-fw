import secrets
import hashlib
from app.domain.user import User

async def validate_user_register_data(data: bool) -> bool:
    if not data.get('username'):
        return False
    elif len(data.get('username')) < 6:
        return False
    elif not data.get('password'):
        return False
    elif len(data.get('password')) < 8:
        return False
    elif not data.get('email'):
        return False
    elif not '@' in data.get('email'):
        return False

    return True

async def generate_salt() -> str:
    return secrets.token_hex(32)

async def hash_password(salt: str, password: str) -> str:
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt), 100000).hex()

async def validate_password(user: User, password: str) -> bool:
    expected_password = await hash_password(user.salt, password)

    return user.password == expected_password

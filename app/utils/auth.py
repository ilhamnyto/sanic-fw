import secrets
import hashlib
from app.domain.user import User
from app.repositories.postgres.auth import get_user_by_username_and_email, get_user_by_phone_number, check_user_password

async def validate_user_register_data(data: dict) -> bool:
    if not data.get('username') or not data.get('password') or not data.get('email'):
        return False
    elif len(data.get('username')) < 6 or len(data.get('password')) < 8 or not '@' in data.get('email'):
        return False
    
    user = await get_user_by_username_and_email(data.get('username'), data.get('email'))
    if user:
        return False
    
    return True

async def validate_update_profile(data: dict) -> bool:
    if not data.get('username') or not data.get('phone_number') or not data.get('email') or \
        not data.get('location'):
        return False
    elif len(data.get('username')) < 6 or len(data.get('phone_number')) < 11 or not '@' in data.get('email'):
        return False
    
    user = await get_user_by_username_and_email(data.get('username'), data.get('email'))
    if user:
        return False
    
    phone_number = await get_user_by_phone_number(data.get('phone_number'))
    if phone_number:
        return False

    return True

async def validate_update_password(data: dict, user_id: int) -> bool:
    if not data.get('password') or not data.get('confirm_password'):
        return False
    elif data.get('password') != data.get('confirm_password'):
        return False
    
    user = await check_user_password(user_id)
    expected_password = await hash_password(user['salt'], data.get('password'))

    return expected_password == user['password']

async def generate_salt() -> str:
    return secrets.token_hex(32)

async def hash_password(salt: str, password: str) -> str:
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()

async def validate_password(user: User, password: str) -> bool:
    expected_password = await hash_password(user.salt, password)

    return user.password == expected_password

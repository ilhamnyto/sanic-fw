from app.config import config
import asyncpg
from app.domain.user import User

async def create_user(user: User) -> None:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    query = """
        INSERT INTO users (username, email, password, salt) VALUES
        ($1, $2, $3, $4)
    """
    await conn.execute(query, user.username, user.email, user.password, user.salt)
    await conn.close()

async def get_user_by_username(username: str) -> User:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    query = """
        SELECT * from users WHERE username = $1
    """
    user = await conn.fetchrow(query, username)
    await conn.close()
    return user

async def get_user_by_email(email: str) -> User:
    conn = await asyncpg.connect(config.POSTGRES_DSN)
    query = """
        SELECT * from users WHERE email = $1
    """
    user = await conn.fetchrow(query, email)
    await conn.close()
    return user
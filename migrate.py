import asyncio
import logging
import time
from app.config import config

import asyncpg

logging.basicConfig(level=logging.INFO)

async def migrate() -> None:
    conn = await asyncpg.connect(config.POSTGRES_DSN)

    queryCreateUserTable = """
        CREATE TABLE IF NOT EXISTS users (
            id serial primary key,
            username varchar(100) NOT NULL,
            first_name varchar(100),
            last_name varchar(100),
            email varchar(100) NOT NULL,
            phone_number varchar(100),
            location varchar(100),
            password varchar(100) NOT NULL,
            salt varchar(100) NOT NULL,
            created_at timestamp,
            updated_at timestamp
        )
    """

    queryCreatePostTable = """
        CREATE TABLE IF NOT EXISTS posts (
            id serial primary key,
            user_id int NOT NULL,
            body text NOT NULL,
            created_at timestamp,
            deleted_at timestamp,
            CONSTRAINT fk_posts
            FOREIGN KEY(user_id)
            REFERENCES users(id)
        )
    """

    await conn.execute(queryCreateUserTable)
    await conn.execute(queryCreatePostTable)
    await conn.close()

if __name__ == '__main__':
    logging.info("Start migrating")
    start = time.time()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(migrate())
    loop.close()
    now = time.time()
    elapsed = now - start
    tmins, tsecs = divmod(elapsed, 60)
    hrs, mins = divmod(tmins, 60)
    logging.info("Time spend: {:.0f} hours {:.0f} mins {:.0f} secs".format(hrs, mins, tsecs))


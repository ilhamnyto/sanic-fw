import os
from dataclasses import dataclass

from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname('.'))
load_dotenv(os.path.join(BASEDIR, '.env'))

@dataclass
class Config:
    HOST: str = os.getenv("HOST")
    PORT: int = int(os.getenv("PORT"))
    DEBUG: bool = os.getenv("DEBUG")
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT"))
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_NAME: str = os.getenv("POSTGRES_NAME")
    POSTGRES_DSN: str = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"

config = Config()
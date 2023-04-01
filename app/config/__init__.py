import os

from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname('.'))
load_dotenv(os.path.join(BASEDIR, '.env'), verbose=True)

DEFAULT_CONFIG = {
    'app': {
        'host': os.getenv("HOST"),
        'port': int(os.getenv("PORT")),
        'debug': os.getenv("DEBUG"),
        'jwt_secret': os.getenv('JWT_SECRET')
    },
    'postgre_db': {
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('POSTGRES_PORT'),
        'name': os.getenv('POSTGRES_NAME'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
    }
}

def get_config(env="development") -> dict:
    config = DEFAULT_CONFIG.copy()
    return config

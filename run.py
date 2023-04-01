from app.config import get_config

from sanic import Sanic
from sanic.response import json
from dotenv import load_dotenv, find_dotenv, dotenv_values

app = Sanic(__name__)

config: dict = get_config()

@app.get('/')
async def index(request):
    return json({"message": "hello"})

if __name__ == '__main__':
    app.run(host=config['app']['host'], port=config['app']['port'], debug=config['app']['debug'])

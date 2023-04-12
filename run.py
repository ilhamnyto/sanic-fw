from app.config import config
from app.routes.auth import auth_bp
from app.routes.user import users_bp
from app.routes.post import post_bp

from sanic import Sanic
from sanic.response import json
import aioredis

app = Sanic(__name__)

app.blueprint(auth_bp)
app.blueprint(users_bp)
app.blueprint(post_bp)

@app.listener('before_server_start')
async def start_redis(app: Sanic):
    app.ctx.redis = await aioredis.from_url('redis://redis')

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

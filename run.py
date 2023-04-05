from app.config import config
from app.routes.auth import auth_bp
from app.routes.user import users_bp
from sanic import Sanic
from sanic.response import json

app = Sanic(__name__)

app.blueprint(auth_bp)
app.blueprint(users_bp)

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

from app.controllers.auth import register_controller, login_controller

from sanic import Blueprint
from sanic.request import Request

auth_bp = Blueprint(name="auth", url_prefix="api/v1/auth")

@auth_bp.post('/register')
async def register(request: Request) -> None:
    data: dict = request.json
    return await register_controller(data=data)

@auth_bp.post('/login')
async def login(request: Request) -> None:
    data: dict = request.json
    return await login_controller(data=data)
from app.controllers.user import all_users_controller, get_users_controller, search_users_controller, my_profile_controller, update_user_profile_controller, update_password_controller
from app.utils.jwt import validate_token

from sanic import Blueprint, Request
from sanic.response import JSONResponse


users_bp = Blueprint("users", url_prefix="api/v1/users")

@users_bp.on_request
async def middleware(request: Request):
    await validate_token(request)

@users_bp.get('/')
async def all_users(request: Request) -> JSONResponse:
    cursor = int(request.args.get("cursor")) if request.args.get("cursor") else None
    
    return await all_users_controller(cursor)

@users_bp.get('/me')
async def my_profile(request: Request) -> JSONResponse:
    user_id = request.ctx.user_id
    redis = request.app.ctx.redis
    return await my_profile_controller(user_id, redis)

@users_bp.get('/search')
async def search_users(request: Request) -> JSONResponse:
    search_query = request.args.get("query")
    cursor = int(request.args.get("cursor")) if request.args.get("cursor") else None
    return await search_users_controller(search_query, cursor)

@users_bp.put('/profile/update')
async def update_profile(request: Request) -> JSONResponse:
    data = request.json
    user_id = request.ctx.user_id
    return await update_user_profile_controller(data, user_id)

@users_bp.put('/profile/update_password')
async def update_password(request: Request) -> JSONResponse:
    data = request.json
    user_id = request.ctx.user_id
    return await update_password_controller(data, user_id)

@users_bp.get('/<username:str>')
async def get_users(request: Request, username: str) -> JSONResponse:
    return await get_users_controller(username)


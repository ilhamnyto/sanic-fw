from app.controllers.user import all_users_controller, get_users_controller, search_users_controller, my_profile_controller, update_user_profile_controller
from app.utils.jwt import validate_token

from sanic import Blueprint, Request
from sanic.response import JSONResponse


users_bp = Blueprint("users", url_prefix="api/v1/users")

@users_bp.on_request
async def middleware(request: Request):
    await validate_token(request)

@users_bp.get('/')
async def all_users(request: Request) -> JSONResponse:
    page_num = int(request.args.get("page_num")) if request.args.get("page_num") else 1
    limit = int(request.args.get("limit")) if request.args.get("limit") else 10
    
    return await all_users_controller(page_num, limit)

@users_bp.get('/me')
async def my_profile(request: Request) -> JSONResponse:
    user_id = request.ctx.user_id
    return await my_profile_controller(user_id)

@users_bp.get('/search')
async def search_users(request: Request) -> JSONResponse:
    search_query = request.args.get("query")
    cursor = int(request.args.get("cursor")) if request.args.get("cursor") else None
    return await search_users_controller(search_query, cursor)

@users_bp.put('/profile/update')
async def update_profile(request: Request) -> JSONResponse:
    data = request.json
    data['user_id'] = request.ctx.user_id
    return await update_user_profile_controller(data)

@users_bp.get('/<username:str>')
async def get_users(request: Request, username: str) -> JSONResponse:
    return await get_users_controller(username)


from app.controllers.user import all_users_controller, get_users_controller, search_users_controller

from sanic import Blueprint, Request

users_bp = Blueprint("users", url_prefix="api/v1/users")

@users_bp.get('/')
async def all_users(request: Request):
    page_num = int(request.args.get("page_num")) if request.args.get("page_num") else 1
    limit = int(request.args.get("limit")) if request.args.get("limit") else 10
    
    return await all_users_controller(page_num, limit)

@users_bp.get('/search')
async def search_users(request: Request):
    search_query = request.args.get("query")
    page_num = int(request.args.get("page_num")) if request.args.get("page_num") else 1
    limit = int(request.args.get("limit")) if request.args.get("limit") else 10
    return await search_users_controller(search_query, page_num, limit)

@users_bp.get('/<username:str>')
async def get_users(request: Request, username: str):
    return await get_users_controller(username)

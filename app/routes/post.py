from app.controllers.post import all_posts_controller, get_posts_controller, search_posts_controller, create_posts_controller, my_posts_controller
from app.utils.jwt import validate_token

from sanic import Request, Blueprint
from sanic.response import JSONResponse

post_bp = Blueprint("posts", url_prefix="api/v1/posts")

@post_bp.on_request
async def middleware(request: Request):
    await validate_token(request)

@post_bp.get('/')
async def all_posts(request: Request) -> JSONResponse:
    cursor = int(request.args.get("cursor")) if request.args.get("cursor") else None
    return await all_posts_controller(cursor)

@post_bp.get('/me')
async def my_posts(request: Request) -> JSONResponse:
    user_id = request.ctx.user_id
    cursor = int(request.args.get("cursor")) if request.args.get("cursor") else None
    return await my_posts_controller(user_id, cursor)

@post_bp.post('/create')
async def create_posts(request: Request) -> JSONResponse:
    data: dict = request.json
    data['user_id'] = request.ctx.user_id
    return await create_posts_controller(data)


@post_bp.get('/<query_str:str>')
async def get_posts(request: Request, query_str: str):
    cursor = int(request.args.get("cursor")) if request.args.get("cursor") else None
    redis = request.app.ctx.redis
    return await get_posts_controller(query_str, cursor, redis)

@post_bp.get('/search')
async def search_posts(request: Request) -> JSONResponse:
    search_query = request.args.get("query")
    cursor = int(request.args.get("cursor")) if request.args.get("cursor") else None
    return await search_posts_controller(search_query, cursor)



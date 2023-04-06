

from sanic import Request, Blueprint
from sanic.response import JSONResponse, json

post_bp = Blueprint("posts", url_prefix="api/v1/posts")

@post_bp.get('/')
async def all_posts(request: Request) -> JSONResponse:
    page_num = int(request.args.get("page_num")) if request.args.get("page_num") else 1
    limit = int(request.args.get("limit")) if request.args.get("limit") else 10
    
    pass

@post_bp.post('/create')
async def create_posts(request: Request) -> JSONResponse:
    pass


@post_bp.get('/<query:str>')
async def get_posts(request: Request, query):
    pass

@post_bp.get('/search')
async def search_posts(request: Request) -> JSONResponse:
    pass



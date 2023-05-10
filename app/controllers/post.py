from dataclasses import asdict
from app.schemas.basic import ErrorResponse
from app.services.post import all_posts_services, create_posts_services, get_single_post_services, get_user_posts_services, search_post_services, my_posts_services
from app.schemas.post import PostResponse, PostData, Paging
from app.schemas.basic import SuccessResponse
from typing import Optional
import json as js

from sanic.response import json, JSONResponse
from sanic.log import logger
import aioredis

async def all_posts_controller(cursor: Optional[int] = None) -> JSONResponse:
    try:
        posts, next = await all_posts_services(cursor)
        data = []
        if posts:
            data = [PostData(id=post.posts_id, username=post.username, body=post.body, created_at=str(post.created_at)) for post in posts]
        if posts and len(posts) > 1:
            paging = Paging(cursor=int(posts[-1:][0].created_at.timestamp()) if next else None, next=next)
        else:
            paging = Paging(cursor=None, next=False)
        success = PostResponse(status=201, data=data, paging=paging)
        return json(asdict(success), status=success.status)
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(message=e, err_code="ERR", status=500)
        return json(asdict(error), status=error.status)
    
async def my_posts_controller(user_id: int, cursor: Optional[int] = None) -> JSONResponse:
    try:
        posts, next = await my_posts_services(user_id, cursor)
        data = []
        if posts:
            data = [PostData(id=post.posts_id, username=post.username, body=post.body, created_at=str(post.created_at)) for post in posts]
        if posts and len(posts) > 1:
            paging = Paging(cursor=int(posts[-1:][0].created_at.timestamp()) if next else None, next=next)
        else:
            paging = Paging(cursor=None, next=False)

        success = PostResponse(status=201, data=data, paging=paging)
        return json(asdict(success), status=success.status)
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(message=e, err_code="ERR", status=500)
        return json(asdict(error), status=error.status)

async def create_posts_controller(data: dict) -> JSONResponse:
    try:
        await create_posts_services(data)
        success = SuccessResponse(message="Post created successdully", status=200)
        return json(asdict(success), status=success.status)
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(message=e, err_code="ERR", status=500)
        return json(asdict(error), status=error.status)

async def get_posts_controller(query_str: str, cursor: int, redis: aioredis.Connection) -> JSONResponse:
    try:
        if query_str[0] == '@':
            posts, next = await get_user_posts_services(query_str[1:], cursor)
            if posts:
                data = [PostData(id=post.posts_id, username=post.username, body=post.body, created_at=str(post.created_at)) for post in posts]
            if posts and len(posts) > 1:
                paging = Paging(cursor=int(posts[-1:][0].created_at.timestamp()) if next else None, next=next)
            else:
                paging = Paging(cursor=None, next=False)
        else:
            posts = await redis.get(f"posts:{query_str}")
            if posts:
                return json(js.loads(posts))

            posts = await get_single_post_services(query_str)
            if posts: 
                data = PostData(id=posts.posts_id, username=posts.username, body=posts.body, created_at=str(posts.created_at))
                paging = Paging(next=False, cursor=None)
            else:
                error = ErrorResponse(message="Posts not found", err_code="ERR_NOT_FOUND", status=404)
                return json(asdict(error), status=error.status)
        
        success = PostResponse(data=data, status=200, paging=paging)
        await redis.set(f"posts:{query_str}", js.dumps(asdict(success)))

        return json(asdict(success), status=success.status)
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(message=e, err_code="ERR", status=500)
        return json(asdict(error), status=error.status)

async def search_posts_controller(search_query: str, cursor: Optional[int] = None) -> JSONResponse:
    try:
        posts, next = await search_post_services(search_query, cursor)
        data = []
        if posts:
            data = [PostData(id=post.posts_id, username=post.username, body=post.body, created_at=str(post.created_at)) for post in posts]
        if posts and len(posts) > 1:
            paging = Paging(cursor=int(posts[-1:][0].created_at.timestamp()) if next else None, next=next)
        else:
            paging = Paging(cursor=None, next=False)
        success = PostResponse(status=201, data=data, paging=paging)
        return json(asdict(success), status=success.status)
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(message=e, err_code="ERR", status=500)
        return json(asdict(error), status=error.status)
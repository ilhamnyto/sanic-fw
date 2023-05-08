from dataclasses import asdict
from app.schemas.basic import ErrorResponse
from app.services.post import all_posts_services, create_posts_services, get_single_post_services, get_user_posts_services, search_post_services, my_posts_services
from app.schemas.post import PostResponse, PostData, Paging
from app.schemas.basic import SuccessResponse
from typing import Optional

from sanic.response import json, JSONResponse
from sanic.log import logger

async def all_posts_controller(cursor: Optional[int] = None) -> JSONResponse:
    try:
        posts, next = await all_posts_services(cursor)
        data = []
        if posts:
            data = [PostData(id=post.posts_id, username=post.username, body=post.body, created_at=post.created_at) for post in posts]
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
        posts = await my_posts_services(user_id, cursor)
        data = []
        if posts:
            data = [PostData(id=post.posts_id, username=post.username, body=post.body, created_at=post.created_at) for post in posts]
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

async def get_posts_controller(query_str: str) -> JSONResponse:
    try:
        if query_str[0] == '@':
            posts = await get_user_posts_services(query_str[1:])
            if posts:
                [PostData(id=post.posts_id, username=post.username, body=post.body, created_at=post.created_at) for post in posts]
            else:
                posts = []
        else:
            posts = await get_single_post_services(query_str)
            if posts: 
                posts = PostData(id=posts.posts_id, username=posts.username, body=posts.body, created_at=posts.created_at)
            else:
                error = ErrorResponse(message="Posts not found", err_code="ERR_NOT_FOUND", status=404)
                return json(asdict(error), status=error.status)
        
        success = PostResponse(data=posts, status=200)
        return json(asdict(success), status=success.status)
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(message=e, err_code="ERR", status=500)
        return json(asdict(error), status=error.status)

async def search_posts_controller(search_query: str) -> JSONResponse:
    try:
        posts = await search_post_services(search_query)
        data = []
        if posts:
            data = [PostData(id=post.posts_id, username=post.username, body=post.body, created_at=post.created_at) for post in posts]
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
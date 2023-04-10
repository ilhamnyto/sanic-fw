from dataclasses import asdict
from app.schemas.basic import ErrorResponse
from app.services.post import all_posts_services, create_posts_services, get_single_post_services, get_user_posts_services, search_post_services
from app.schemas.post import PostResponse
from app.schemas.basic import SuccessResponse
from typing import Optional

from sanic.response import json, JSONResponse
from sanic.log import logger

async def all_posts_controller(limit: int, cursor: Optional[int] = None) -> JSONResponse:
    try:
        posts = await all_posts_services(limit, cursor)
        success = PostResponse(data=posts, status=200)
        # return json(asdict(posts), status=success.status)
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(message=e, err_code="ERR", status=500)
        # return json(asdict(error), status=error.status)

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
            posts = await get_user_posts_services(query_str[:1])
        else:
            posts = await get_single_post_services(query_str)
        success = PostResponse(data=posts, status=200)
        return json(asdict(success), status=success.status)
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(message=e, err_code="ERR", status=500)
        return json(asdict(error), status=error.status)

async def search_posts_controller(query_str: str) -> JSONResponse:
    try:
        posts = await search_post_services(query_str)
        success = PostResponse(data=posts, status=200)
        return json(asdict(success), status=success.status)
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(message=e, err_code="ERR", status=500)
        return json(asdict(error), status=error.status)
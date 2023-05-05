from app.schemas.user import UserResponse, User, Paging
from app.services.user import all_users_services, get_users_services, search_users_services, my_profile_services
from app.schemas.basic import ErrorResponse
from dataclasses import asdict
from datetime import datetime
import time

from sanic.response import json, JSONResponse
from sanic.log import logger

async def all_users_controller(cursor: int) -> JSONResponse:
    try:
        users, next = await all_users_services(cursor)
        data = []
        if users:
            data = [ User(username=user.username, email=user.email, created_at=str(user.created_at)) for user in users ]
        if users and len(users) > 1:
            paging = Paging(cursor=int(users[-1:][0].created_at.timestamp()) if next else None, next=next)
        else:
            paging = Paging(cursor=None, next=False)
        success = UserResponse(status=201, data=data, paging=paging)
        return json(asdict(success), status=success.status)
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(status=500, message="error occured.", err_code="ERR")
        return json(asdict(error), error.status)
    
async def my_profile_controller(user_id: int) -> JSONResponse:
    try:
        user = await my_profile_services(user_id)
        if user:
            data = User(username=user.username, email=user.email, created_at=str(user.created_at))
        else:
            error = ErrorResponse(status=404, message="User not found.", err_code="ERR_NOT_FOUND")
            return json(asdict(error), error.status)    
        
        success = UserResponse(status=201, data=data, paging=Paging(cursor=None, next=False))
        return json(asdict(success), status=success.status)
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(status=500, message="error occured.", err_code="ERR")
        return json(asdict(error), error.status)
        

async def get_users_controller(username: str) -> JSONResponse:
    try:
        user = await get_users_services(username)
        data = []
        if user:
            data = [ User(username=user.username, email=user.email, created_at=str(user.created_at)) ]
        success = UserResponse(status=201, data=data, paging=Paging(cursor=None, next=False))
        return json(asdict(success), status=success.status)
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(status=500, message="error occured.", err_code="ERR")
        return json(asdict(error), error.status)


async def search_users_controller(search_query: int, cursor: str) -> JSONResponse:
    try:
        users, next = await search_users_services(search_query, cursor)
        data = []
        if users:
            data = [ User(username=user.username, email=user.email, created_at=str(user.created_at)) for user in users ]
        if users and len(users) > 1:
            paging = Paging(cursor=int(users[-1:][0].created_at.timestamp()) if next else None, next=next)
        else:
            paging = Paging(cursor=None, next=False)
        success = UserResponse(status=201, data=data, paging=paging)
        return json(asdict(success), status=success.status)
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(status=500, message="error occured.", err_code="ERR")
        return json(asdict(error), error.status)
    
async def update_user_profile_controller(data: dict) -> JSONResponse:
    try:
        pass
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(status=500, message="error occured.", err_code="ERR")
        return json(asdict(error), error.status)

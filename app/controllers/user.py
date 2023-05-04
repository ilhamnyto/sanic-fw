from app.schemas.user import UserResponse, User, Paging
from app.services.user import all_users_services, get_users_services, search_users_services, my_profile_services
from app.schemas.basic import ErrorResponse
from dataclasses import asdict
from datetime import datetime
import time

from sanic.response import json, JSONResponse
from sanic.log import logger

async def all_users_controller(page_num: int = 1, limit: int = 10) -> JSONResponse:
    try:
        users = await all_users_services(page_num, limit)
        data = []
        if users:
            data = [ User(username=user.username, email=user.email) for user in users ]
        
        success = UserResponse(status=201, data=data)
        return json(asdict(success), status=success.status)
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(status=500, message="error occured.", err_code="ERR")
        return json(asdict(error), error.status)
    
async def my_profile_controller(user_id: int) -> JSONResponse:
    try:
        user = await my_profile_services(user_id)
        if user:
            data = User(username=user.username, email=user.email, created_at=user.created_at)
        else:
            error = ErrorResponse(status=404, message="User not found.", err_code="ERR_NOT_FOUND")
            return json(asdict(error), error.status)    
        
        success = UserResponse(status=201, data=data)
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
        success = UserResponse(status=201, data=data, paging=None)
        return json(asdict(success), status=success.status)
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(status=500, message="error occured.", err_code="ERR")
        return json(asdict(error), error.status)


async def search_users_controller(search_query: int, cursor: str) -> JSONResponse:
    try:
        users = await search_users_services(search_query, cursor)
        data = []
        if users:
            data = [ User(username=user.username, email=user.email, created_at=str(user.created_at)) for user in users ]
        if users and len(users) > 1:
            print(int(time.mktime(datetime.strptime(str(users[-1:][0].created_at), '%Y-%m-%d %H:%M:%S.%f').timetuple())))
            print(time.mktime(datetime.strptime(str(users[-1:][0].created_at), '%Y-%m-%d %H:%M:%S.%f').timetuple()))
            print(datetime.strptime(str(users[-1:][0].created_at), '%Y-%m-%d %H:%M:%S.%f'))
            print(datetime.strptime(str(users[-1:][0].created_at), '%Y-%m-%d %H:%M:%S.%f').timetuple())
            paging = Paging(current=cursor, next=int(time.mktime(datetime.strptime(str(users[-1:][0].created_at), '%Y-%m-%d %H:%M:%S.%f').timetuple())))
        else:
            paging = Paging(current=cursor, next=None)
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

from app.schemas.user import UserResponse, User
from app.services.user import all_users_services, get_users_services, search_users_services, my_profile_services
from app.schemas.basic import ErrorResponse
from dataclasses import asdict

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
            data = User(username=user.username, email=user.email)
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
            data = [ User(username=user.username, email=user.email) ]
        
        success = UserResponse(status=201, data=data)
        return json(asdict(success), status=success.status)
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(status=500, message="error occured.", err_code="ERR")
        return json(asdict(error), error.status)


async def search_users_controller(search_query: str, page_num: int = 1, limit: int = 10) -> JSONResponse:
    try:
        users = await search_users_services(search_query, page_num, limit)
        data = []
        if users:
            data = [ User(username=user.username, email=user.email) for user in users ]
        
        success = UserResponse(status=201, data=data)
        return json(asdict(success), status=success.status)
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(status=500, message="error occured.", err_code="ERR")
        return json(asdict(error), error.status)

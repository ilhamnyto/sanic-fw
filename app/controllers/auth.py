from dataclasses import asdict
from app.schemas.basic import ErrorResponse, SuccessResponse
from app.schemas.auth import UserLoginResponse
from app.utils.auth import validate_user_register_data
from app.services.auth import register_services, login_services
from app.config import config
from datetime import datetime, timedelta

from sanic.response import json, JSONResponse
from sanic.log import logger
import jwt

async def register_controller(data: dict) -> JSONResponse:
    try:
        if await validate_user_register_data(data):
            await register_services(data)
        else:
            error = ErrorResponse(status=500, message="Invalid user input.", err_code="ERR_USER_INPUT")
            return json(asdict(error), error.status)

        success = SuccessResponse(status=201, message="created successfully")
        return json(asdict(success), success.status)
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(status=500, message="error occured.", err_code="ERR")
        return json(asdict(error), error.status)

async def login_controller(data: dict) -> JSONResponse:
    try:
        user = await login_services(data)
        if not user:
            error = ErrorResponse(status=403, message="Wrong username or password.", err_code="ERR_NOT_AUTHENTICATED")
            return json(asdict(error), error.status)
        
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=10)
        }
        token = jwt.encode(payload, config.SECRET_KEY, algorithm='HS256')

        success = UserLoginResponse(status=200, access_token=token)
        return json(asdict(success), success.status)
    except Exception as e:
        logger.error(e)
        error = ErrorResponse(status=500, message="error occured.", err_code="ERR")
        return json(asdict(error), error.status)
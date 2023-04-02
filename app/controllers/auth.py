from dataclasses import asdict
from app.schemas.basic import ErrorResponse, SuccessResponse
from app.utils.auth import validate_user_register_data
from app.services.auth import register_services, login_services

from sanic.response import json, JSONResponse
from sanic.log import logger

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
        logger(e)
        error = ErrorResponse(status=500, message="error occured.", err_code="ERR")
        return json(asdict(error), error.status)

async def login_controller(data: dict) -> JSONResponse:
    try:
        user = await login_services(data)
        if not user:
            error = ErrorResponse(status=403, message="Wrong username or password.", err_code="ERR_NOT_AUTHENTICATED")
            return json(asdict(error), error.status)
            
        success = SuccessResponse(status=200, message="login successfully")
        return json(asdict(success), success.status)
    except Exception as e:
        logger(e)
        error = ErrorResponse(status=500, message="error occured.", err_code="ERR")
        return json(asdict(error), error.status)
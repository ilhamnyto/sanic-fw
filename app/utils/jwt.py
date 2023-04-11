import jwt
from app.config import config

from sanic import Request, exceptions
async def validate_token(request: Request):
    auth_header = request.headers.get('Authorization')

    if auth_header is None:
        raise exceptions.Unauthorized('Missing authorization header.')
    try:
        token = auth_header.split(' ')[1]
    except IndexError:
        raise exceptions.Unauthorized('Invalid Authorization Header')
    
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=['HS256'])
    except jwt.exceptions.ExpiredSignatureError:
        raise exceptions.Unauthorized('Token has expired')
    except jwt.exceptions.InvalidSignatureError:
        raise exceptions.Unauthorized('Invalid token')
    
    request.ctx.user_id = payload.get('user_id')

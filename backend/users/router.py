import typing as tp

import fastapi
from fastapi import security

from backend import config
from backend import database as db
from backend import exceptions
from backend.users import auth
from backend.users import models
from backend.users import schemas

ROUTER = fastapi.APIRouter(prefix='/auth', tags=['Auth'])

oauth_form = tp.Annotated[security.OAuth2PasswordRequestForm, fastapi.Depends()]
settings = config.get_settings()

@ROUTER.post('/register', status_code=fastapi.status.HTTP_201_CREATED)
async def register_user(user_data: schemas.UserRegistration, db: db.SessionDep) -> dict[str, str]:
    user = await models.user_crud.exists(db, email=user_data.email)
    if user:
        raise exceptions.UserAlreadyExistsException
    
    if user_data.password != user_data.password_check:
        raise exceptions.PasswordMismatchException
    
    
    user_create = user_data.model_dump()
    hashed_password = auth.get_password_hash(user_data.password)

    user_create['hashed_password'] = hashed_password
    del user_create['password']
    del user_create['password_check']

    user_internal = schemas.UserRegistrationInternal(**user_create)

    await models.user_crud.create(db, user_internal)

    return {'name': user_internal.name, 'status': 'success'}


@ROUTER.post('/login', response_model=schemas.Token)
async def login_access_token(response: fastapi.Response, form_data: oauth_form, db: db.SessionDep) -> dict[str, str]:
    user = await auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise exceptions.UnauthorizedException

    access_token = await auth.create_tokens({'sub': user['email']})
    refresh_token = await auth.create_tokens({'sub': user['email']}, 'refresh')
    max_age = settings.refresh_token_expire_days * 24 * 60 * 60

    response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, samesite='lax', max_age=max_age)

    return {'access_token': access_token, 'token_type': 'bearer'}


@ROUTER.post('/refresh')
async def refresh_access_token(request: fastapi.Request, db: db.SessionDep) -> dict[str, str]:
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        raise exceptions.RefreshTokenMissingException
    
    email = await auth.verify_token(refresh_token, db)
    if not email:
        raise exceptions.RefreshTokenMissingException
    
    new_access_token = await auth.create_tokens({'sub': email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}

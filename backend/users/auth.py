import datetime as dt
import typing as tp

import jose
from jose import jwt
from passlib import context

from backend import config
from backend import database as db
from backend.users import models

settings = config.get_settings()

PWD_CONTEXT = context.CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def verify_password(raw_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(raw_password, hashed_password)


async def authenticate_user(email: str, password: str, db: db.SessionDep) -> dict | None:
    db_user: dict | None = await models.user_crud.get(db=db, email=email, is_deleted=False)

    if not db_user:
        return None
    
    if not verify_password(password, db_user['hashed_password']):
        return None
    
    return db_user


async def create_tokens(
        data: dict[str, tp.Any],
        type: tp.Literal['access', 'refresh'] = 'access',
        expires_delta: dt.timedelta | None = None
) -> str:
    to_encode = data.copy()
    now = dt.datetime.now(dt.UTC).replace(tzinfo=None)
    if expires_delta:
        expire = now + expires_delta
    else:
        if type == 'access':
            expire = now + dt.timedelta(minutes=settings.access_token_expire_minutes)
        else:
            expire = now + dt.timedelta(days=settings.refresh_token_expire_days)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, settings.algorithm)
    return encoded_jwt


async def verify_token(token: str, db: db.SessionDep) -> str | None:
    try:
        payload = jwt.decode(token, settings.secret_key, [settings.algorithm])
        email: str | None = payload.get('sub')
        if not email:
            return None
        return email
    except jose.JWTError:
        return None

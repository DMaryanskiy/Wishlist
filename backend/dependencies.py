import typing as tp

import fastapi

from backend import database as db
from backend import exceptions
from backend.users import auth
from backend.users import models


async def get_current_user(
    token: tp.Annotated[str, fastapi.Depends(auth.oauth2_scheme)],
    db: db.SessionDep
) -> dict[str, str]:
    email = await auth.verify_token(token, db)
    if not email:
        raise exceptions.RefreshTokenMissingException
    
    user: dict[str, str] | None = await models.user_crud.get(db, email=email, is_deleted=False)
    if user:
        return user
    
    raise exceptions.UserAlreadyDeletedException

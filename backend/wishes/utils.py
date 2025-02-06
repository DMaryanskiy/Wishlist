from backend import database as db
from backend import dependencies
from backend import exceptions
from backend.wishes import models

async def is_secret_manager(
    is_secret: bool,
    wish_id: int,
    current_user: dependencies.CurrentUserDep,
    db: db.SessionDep,
):
    is_own_wish = await models.wishes_crud.exists(db, id=wish_id, user=current_user.id)
    if not is_own_wish:
        raise exceptions.EditForbiddenException
    
    await models.wishes_crud.update(db, {'is_secret': is_secret}, id=wish_id)

async def is_gifted_manager(
    is_gifted: bool,
    wish_id: int,
    current_user: dependencies.CurrentUserDep,
    db: db.SessionDep,
):
    is_own_wish = await models.wishes_crud.exists(db, id=wish_id, user=current_user.id)
    if not is_own_wish:
        raise exceptions.EditForbiddenException
    
    await models.wishes_crud.update(db, {'is_gifted': is_gifted}, id=wish_id)

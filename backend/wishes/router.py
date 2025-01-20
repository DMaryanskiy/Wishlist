import fastapi

from backend import database as db
from backend import dependencies
from backend import exceptions
from backend.wishes import models
from backend.wishes import schemas

ROUTER = fastapi.APIRouter(prefix='/wishes', tags=['Wishes'])


@ROUTER.post('/create', response_model=schemas.WishesCreate, status_code=fastapi.status.HTTP_201_CREATED)
async def create_wish(
    wish_data: schemas.WishesBase,
    current_user: dependencies.CurrentUserDep,
    db: db.SessionDep,
) -> schemas.WishesCreate:
    wish_dict = wish_data.model_dump()
    wishes_create = schemas.WishesCreate(**wish_dict, user=current_user.id)

    await models.wishes_crud.create(db, wishes_create)

    wishes_create.user = current_user.email
    return wishes_create


@ROUTER.put('/{wish_id}/edit', response_model=schemas.WishesBase)
async def edit_wish(
    wish_id: int,
    wish_data: schemas.WishesBase,
    current_user: dependencies.CurrentUserDep,
    db: db.SessionDep,
) -> schemas.WishesBase:
    current_wish: schemas.WishesCreate = await models.wishes_crud.get(db, schema_to_select=schemas.WishesCreate, return_as_model=True, id=wish_id)
    if current_wish.user != current_user.id:
        raise exceptions.EditForbiddenException
    
    edit_data = wish_data.model_dump(exclude_none=True)
    await models.wishes_crud.update(db, edit_data, id=wish_id)

    return schemas.WishesBase(**edit_data)


@ROUTER.delete('/{wish_id}', status_code=fastapi.status.HTTP_204_NO_CONTENT)
async def delete_wish(
    wish_id: int,
    current_user: dependencies.CurrentUserDep,
    db: db.SessionDep,
):
    current_wish: schemas.WishesCreate = await models.wishes_crud.get(db, schema_to_select=schemas.WishesCreate, return_as_model=True, id=wish_id)
    if current_wish.user != current_user.id:
        raise exceptions.EditForbiddenException
    
    await models.wishes_crud.db_delete(db, id=wish_id)

    return {'message': 'Желание удалено!'}


@ROUTER.get('/by_substring', response_model=list[schemas.WishesBase])
async def get_wishes_by_substring(
    db: db.SessionDep,
    substring: str = '',
):
    if not substring:
        return []
    
    wishes = await models.wishes_crud.get_multi(
        db,
        name__like=f'%{substring}%',
        return_as_model=True,
        schema_to_select=schemas.WishesBase,
    )
    return wishes['data']


@ROUTER.get('/{user_id}', response_model=list[schemas.WishesBase])
async def get_wishes_by_user(
    user_id: int,
    db: db.SessionDep,
):
    wishes = await models.wishes_crud.get_multi(
        db,
        user=user_id,
        return_as_model=True,
        schema_to_select=schemas.WishesBase,
    )
    return wishes['data']

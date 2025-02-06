import fastapi

from backend import database as db
from backend import dependencies
from backend import exceptions
from backend.categories import models as cat_models
from backend.categories import schemas as cat_schemas
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


@ROUTER.get('/by_category/{name}', response_model=list[schemas.WishesBase])
async def get_wishes_by_category(
    name: str,
    current_user: dependencies.CurrentUserDep,
    db: db.SessionDep,
):
    user_category: cat_schemas.CategoryEnhanced = await cat_models.user_categories_crud.get(
        db,
        return_as_model=True,
        schema_to_select=cat_schemas.CategoryEnhanced,
        name=name,
        user=current_user.id
    )

    wishes_ids_raw = await cat_models.wish_categories_crud.get_multi(
        db,
        return_as_model=True,
        schema_to_select=cat_schemas.WishId,
        category_id=user_category.category_id,
    )

    wishes_ids: list[cat_schemas.WishId] = wishes_ids_raw['data']
    wishes_ids = [obj.wish for obj in wishes_ids]

    wishes = await models.wishes_crud.get_multi(
        db,
        id__in=wishes_ids,
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


@ROUTER.post('/{wish_id}/reserve', response_model=schemas.WishesReserve)
async def reserve_wishes(
    wish_id: int,
    current_user: dependencies.CurrentUserDep,
    db: db.SessionDep,
):
    is_reserved = await models.reserved_wishes_crud.exists(db, wish=wish_id)
    if is_reserved:
        raise exceptions.WishAlreadyReservedException
    
    is_own_wish = await models.wishes_crud.exists(db, id=wish_id, user=current_user.id)
    if is_own_wish:
        raise exceptions.ReserveForbiddenException

    reserve_create = schemas.WishesReserve(user=current_user.id, wish=wish_id)
    await models.reserved_wishes_crud.create(db, reserve_create)
    await models.wishes_crud.update(db, {'reserved': True}, id=wish_id)

    reserve_create.user = current_user.email
    return reserve_create


@ROUTER.delete('/{wish_id}/reserve', status_code=fastapi.status.HTTP_204_NO_CONTENT)
async def reserve_wishes(
    wish_id: int,
    current_user: dependencies.CurrentUserDep,
    db: db.SessionDep,
):
    is_by_me_reserved = await models.reserved_wishes_crud.exists(db, wish=wish_id, user=current_user.id)
    if not is_by_me_reserved:
        raise exceptions.WishNotReservedException
    
    await models.reserved_wishes_crud.db_delete(db, wish=wish_id)
    await models.wishes_crud.update(db, {'reserved': False}, id=wish_id)

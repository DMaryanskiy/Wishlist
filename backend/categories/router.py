import fastapi

from backend import database as db
from backend import dependencies
from backend import exceptions
from backend.categories import models
from backend.categories import schemas
from backend.wishes import models as wish_models
from backend.wishes import schemas as wish_schemas

ROUTER = fastapi.APIRouter(prefix='/categories', tags=['Categories'])


@ROUTER.post('/bind', response_model=schemas.CategoryBind, status_code=fastapi.status.HTTP_201_CREATED)
async def bind_wish(
    bind_data: schemas.CategoryBind,
    current_user: dependencies.CurrentUserDep,
    db: db.SessionDep,
):
    bind = await models.wish_categories_crud.exists(db, category_id=bind_data.category_id, wish=bind_data.wish)
    if bind:
        raise exceptions.BindAlreadyExistsException

    current_category: schemas.CategoryCreate = await models.user_categories_crud.get(
        db,
        schema_to_select=schemas.CategoryCreate,
        return_as_model=True,
        category_id=bind_data.category_id,
    )
    if current_category.user != current_user.id:
        raise exceptions.EditForbiddenException
    
    current_wish: wish_schemas.WishesCreate = await wish_models.wishes_crud.get(
        db,
        schema_to_select=wish_schemas.WishesCreate,
        return_as_model=True,
        id=bind_data.wish,
    )
    if current_wish.user != current_user.id:
        raise exceptions.EditForbiddenException
    
    await models.wish_categories_crud.create(db, bind_data)

    return bind_data


@ROUTER.delete('/bind', status_code=fastapi.status.HTTP_204_NO_CONTENT)
async def unbind(
    current_user: dependencies.CurrentUserDep,
    db: db.SessionDep,
    category_id: int = 0,
    wish_id: int = 0,
):
    if not category_id or not wish_id:
        raise exceptions.QueryMissedException

    bind = await models.wish_categories_crud.exists(db, category_id=category_id, wish=wish_id)
    if not bind:
        raise exceptions.BindDoesNotExistException

    current_category: schemas.CategoryCreate = await models.user_categories_crud.get(
        db,
        schema_to_select=schemas.CategoryCreate,
        return_as_model=True,
        category_id=category_id,
    )
    if current_category.user != current_user.id:
        raise exceptions.EditForbiddenException
    
    current_wish: wish_schemas.WishesCreate = await wish_models.wishes_crud.get(
        db,
        schema_to_select=wish_schemas.WishesCreate,
        return_as_model=True,
        id=wish_id,
    )
    if current_wish.user != current_user.id:
        raise exceptions.EditForbiddenException
    
    await models.wish_categories_crud.db_delete(db, category_id=category_id, wish=wish_id)

    return {'message': 'Привязка удалена!'}


@ROUTER.post('/create', response_model=schemas.CategoryCreate, status_code=fastapi.status.HTTP_201_CREATED)
async def create_category(
    category_data: schemas.CategoryBase,
    current_user: dependencies.CurrentUserDep,
    db: db.SessionDep,
) -> schemas.CategoryCreate:
    category = await models.user_categories_crud.exists(db, name=category_data.name, user=current_user.id)
    if category:
        raise exceptions.CategoryAlreadyExistsException

    categories_create = schemas.CategoryCreate(name=category_data.name, user=current_user.id)

    await models.user_categories_crud.create(db, categories_create)

    categories_create.user = current_user.email
    return categories_create


@ROUTER.put('/{category_id}/edit', response_model=schemas.CategoryBase)
async def edit_category(
    category_id: int,
    category_data: schemas.CategoryBase,
    current_user: dependencies.CurrentUserDep,
    db: db.SessionDep,
) -> schemas.CategoryBase:
    category = await models.user_categories_crud.exists(db, category_id=category_id, user=current_user.id)
    if not category:
        raise exceptions.EditForbiddenException
    
    edit_data = category_data.model_dump()
    await models.user_categories_crud.update(db, edit_data, category_id=category_id)

    return schemas.CategoryBase(**edit_data)


@ROUTER.delete('/{category_id}', status_code=fastapi.status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    current_user: dependencies.CurrentUserDep,
    db: db.SessionDep,
):
    current_category: schemas.CategoryCreate = await models.user_categories_crud.get(db, schema_to_select=schemas.CategoryCreate, return_as_model=True, category_id=category_id)
    if current_category.user != current_user.id:
        raise exceptions.EditForbiddenException
    
    await models.user_categories_crud.db_delete(db, category_id=category_id)

    return {'message': 'Категория удалена!'}

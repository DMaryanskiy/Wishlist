import fastapi

from backend import database as db
from backend import dependencies
from backend import exceptions
from backend.categories import models
from backend.categories import schemas

ROUTER = fastapi.APIRouter(prefix='/categories', tags=['Categories'])


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

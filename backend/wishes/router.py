import fastapi

from backend import database as db
from backend import dependencies
from backend.wishes import models
from backend.wishes import schemas

ROUTER = fastapi.APIRouter(prefix='/wishes', tags=['Wishes'])


@ROUTER.post('/create', status_code=fastapi.status.HTTP_201_CREATED)
async def create_wish(
    wish_data: schemas.WishesBase,
    current_user: dependencies.CurrentUserDep,
    db: db.SessionDep
) -> dict[str, str]:
    wish_dict = wish_data.model_dump()
    wishes_create = schemas.WishesCreate(**wish_dict, user=current_user.id)

    await models.wishes_crud.create(db, wishes_create)

    return {'name': wishes_create.name, 'user': current_user.name}

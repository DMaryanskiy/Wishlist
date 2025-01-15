import typing as tp

import fastapi

from backend import database as db
from backend import dependencies
from backend import exceptions
from backend.subscriptions import models
from backend.subscriptions import schemas

ROUTER = fastapi.APIRouter(prefix='/subscribe', tags=['Subscription'])


@ROUTER.post('/{user_id}', status_code=fastapi.status.HTTP_201_CREATED, response_model=schemas.SubscriptionBase)
async def subscribe(user_id: int, current_user: dependencies.CurrentUserDep, db: db.SessionDep) -> dict[str, str]:
    subscription = await models.subscriptions_crud.exists(db, subscriber=current_user.id, subscription=user_id)
    if subscription:
        raise exceptions.SubscriptionAlreadyExistsException
    
    subscription_create = schemas.SubscriptionBase(subscriber=current_user.id, subscription=user_id)
    await models.subscriptions_crud.create(db, subscription_create)

    return subscription_create

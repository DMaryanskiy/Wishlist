import typing as tp

import fastapi

from backend import database as db
from backend import dependencies
from backend import exceptions
from backend.subscriptions import models
from backend.subscriptions import schemas
from backend.users import models as user_models
from backend.users import schemas as user_schemas

ROUTER = fastapi.APIRouter(prefix='/subscribe', tags=['Subscription'])


@ROUTER.post('/{user_id}', status_code=fastapi.status.HTTP_201_CREATED, response_model=schemas.SubscriptionBase)
async def subscribe(user_id: int, current_user: dependencies.CurrentUserDep, db: db.SessionDep) -> dict[str, str]:
    subscription = await models.subscriptions_crud.exists(db, subscriber=current_user.id, subscription=user_id)
    if subscription:
        raise exceptions.SubscriptionAlreadyExistsException
    
    subscription_create = schemas.SubscriptionBase(subscriber=current_user.id, subscription=user_id)
    await models.subscriptions_crud.create(db, subscription_create)

    return subscription_create


@ROUTER.get('/{user_id}/get/subscribers', response_model=list[user_schemas.UserBase])
async def get_subscribers(user_id: int, db: db.SessionDep):
    subscribers_ids_raw = await models.subscriptions_crud.get_multi(
        db,
        subscription=user_id,
        return_as_model=True,
        schema_to_select=schemas.SubscriberId,
    )

    subscribers_ids: list[schemas.SubscriberId] = subscribers_ids_raw['data']
    subscribers_ids = [obj.subscriber for obj in subscribers_ids]

    users = await user_models.user_crud.get_multi(
        db,
        id__in=subscribers_ids,
        return_as_model=True,
        schema_to_select=user_schemas.UserBase,
    )
    return users['data']


@ROUTER.get('/{user_id}/get/subscriptions', response_model=list[user_schemas.UserBase])
async def get_subscriptions(user_id: int, db: db.SessionDep):
    subscribers_ids_raw = await models.subscriptions_crud.get_multi(
        db,
        subscriber=user_id,
        return_as_model=True,
        schema_to_select=schemas.SubscriptionId,
    )

    subscriptions_ids: list[schemas.SubscriptionId] = subscribers_ids_raw['data']
    subscriptions_ids = [obj.subscription for obj in subscriptions_ids]

    users = await user_models.user_crud.get_multi(
        db,
        id__in=subscriptions_ids,
        return_as_model=True,
        schema_to_select=user_schemas.UserBase,
    )
    return users['data']

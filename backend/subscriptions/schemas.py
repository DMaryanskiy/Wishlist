import pydantic


class SubscriptionBase(pydantic.BaseModel):
    subscriber: int = pydantic.Field(..., description='Идентификатор подписчика')
    subscription: int = pydantic.Field(..., description='Идентификатор подписки')


class SubscriberId(pydantic.BaseModel):
    subscriber: int = pydantic.Field(..., description='Идентификатор подписчика/подписки')


class SubscriptionId(pydantic.BaseModel):
    subscription: int = pydantic.Field(..., description='Идентификатор подписчика/подписки')

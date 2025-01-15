import pydantic


class SubscriptionBase(pydantic.BaseModel):
    subscriber: int = pydantic.Field(..., description='Идентификатор подписчика')
    subscription: int = pydantic.Field(..., description='Идентификатор подписки')

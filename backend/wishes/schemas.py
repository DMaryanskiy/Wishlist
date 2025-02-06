import pydantic


class WishesBase(pydantic.BaseModel):
    name: str = pydantic.Field(..., min_length=3, max_length=50, description='Имя, от 3 до 50 символов')
    link: str | None = pydantic.Field('', description='Ссылка на покупку желания')
    description: str | None = pydantic.Field('', description='Описание желания')
    image: str | None = pydantic.Field('', description='Ссылка на картинку желания')


class WishesCreate(WishesBase):
    user: int = pydantic.Field(..., description='Пользователь, создавший желание')


class WishesReserve(pydantic.BaseModel):
    user: int = pydantic.Field(..., description='Пользователь, зарезервировавший желание')
    wish: int = pydantic.Field(..., description='Желание в резерве')

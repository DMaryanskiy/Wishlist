import pydantic


class UserBase(pydantic.BaseModel):
    email: pydantic.EmailStr = pydantic.Field(..., description='Электронная почта')
    name: str = pydantic.Field(..., min_length=3, max_length=50, description='Имя, от 3 до 50 символов')


class UserRegistration(UserBase):
    password: str = pydantic.Field(..., min_length=5, max_length=50, description='Пароль, от 5 до 50 знаков')
    password_check: str = pydantic.Field(..., min_length=5, max_length=50, description='Пароль, от 5 до 50 знаков')


class UserRegistrationInternal(UserBase):
    hashed_password: str = pydantic.Field(..., description='Захешированный пароль')


class UserEditBase(pydantic.BaseModel):
    email: pydantic.EmailStr | None = pydantic.Field(None, description='Электронная почта')
    name: str | None = pydantic.Field(None, min_length=3, max_length=50, description='Имя, от 3 до 50 символов')


class UserEdit(UserEditBase):
    password: str | None = pydantic.Field(None, min_length=5, max_length=50, description='Пароль, от 5 до 50 знаков')


class UserEditInternal(UserEditBase):
    hashed_password: str | None = pydantic.Field(None, description='Захешированный пароль')


# -------------- token --------------
class Token(pydantic.BaseModel):
    access_token: str
    token_type: str

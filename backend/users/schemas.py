import pydantic


class UserRegistration(pydantic.BaseModel):
    email: pydantic.EmailStr = pydantic.Field(..., description='Электронная почта')
    password: str = pydantic.Field(..., min_length=5, max_length=50, description='Пароль, от 5 до 50 знаков')
    password_check: str = pydantic.Field(..., min_length=5, max_length=50, description='Пароль, от 5 до 50 знаков')
    name: str = pydantic.Field(..., min_length=3, max_length=50, description='Имя, от 3 до 50 символов')

import fastapi

from backend import exceptions
from backend.users import auth
from backend.users import dao
from backend.users import schemas

ROUTER = fastapi.APIRouter(prefix='/auth', tags=['Auth'])


@ROUTER.post('/register')
async def register_user(user_data: schemas.UserRegistration) -> dict[str, str]:
    user = await dao.UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise exceptions.UserAlreadyExistsException
    
    if user_data.password != user_data.password_check:
        raise exceptions.PasswordMismatchException('Пароли не совпадают')
    
    hashed_password = auth.get_password_hash(user_data.password)
    await dao.UsersDAO.add(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
    )

    return {'message': 'Вы успешно зарегистрированы!'}

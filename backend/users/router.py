import fastapi
import fastcrud

from backend import database as db
from backend import exceptions
from backend.users import auth
from backend.users import models
from backend.users import schemas

ROUTER = fastapi.APIRouter(prefix='/auth', tags=['Auth'])

user_crud = fastcrud.FastCRUD(models.Users)

@ROUTER.post('/register', status_code=fastapi.status.HTTP_201_CREATED)
async def register_user(user_data: schemas.UserRegistration, session: db.SessionDep) -> dict[str, str]:
    user = await user_crud.exists(session, email=user_data.email)
    if user:
        raise exceptions.UserAlreadyExistsException
    
    if user_data.password != user_data.password_check:
        raise exceptions.PasswordMismatchException('Пароли не совпадают')
    
    user_create = user_data.model_dump()
    hashed_password = auth.get_password_hash(user_data.password)

    user_create['hashed_password'] = hashed_password
    del user_create['password']
    del user_create['password_check']

    user_internal = schemas.UserRegistrationInternal(**user_create)

    await user_crud.create(session, user_internal)

    return {'name': user_internal.name, 'status': 'success'}

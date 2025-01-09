import fastapi
from fastapi import status


UserAlreadyExistsException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Пользователь уже существует')

PasswordMismatchException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Пароли не совпадают!')

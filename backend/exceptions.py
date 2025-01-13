import fastapi
from fastapi import status


UserAlreadyExistsException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Пользователь уже существует!')

PasswordMismatchException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Пароли не совпадают!')

UnauthorizedException = fastapi.HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверная почта или пароль!')

RefreshTokenMissingException = fastapi.HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Отсутствует токен обновления или он некорректный!')

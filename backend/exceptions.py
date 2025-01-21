import fastapi
from fastapi import status


UserAlreadyExistsException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Пользователь уже существует!')

SubscriptionAlreadyExistsException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Подписка уже существует!')

CategoryAlreadyExistsException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Категория уже существует!')

SubscriptionDoesNotExistException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Подписки не существует!')

PasswordMismatchException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Пароли не совпадают!')

UnauthorizedException = fastapi.HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверная почта или пароль!')

RefreshTokenMissingException = fastapi.HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Отсутствует токен обновления или он некорректный!')

UserAlreadyDeletedException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Пользователь был удален!')

InvalidTokenException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Некорректный токен или он отсутствует!')

EditForbiddenException = fastapi.HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Изменение не своего желания или категории запрещено!')

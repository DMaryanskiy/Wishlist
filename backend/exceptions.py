import fastapi
from fastapi import status


UserAlreadyExistsException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Пользователь уже существует!')

SubscriptionAlreadyExistsException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Подписка уже существует!')

CategoryAlreadyExistsException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Категория уже существует!')

BindAlreadyExistsException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Желание уже привязано к этой категории!')

BindDoesNotExistException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Желание уже отвязано от этой категории!')

SubscriptionDoesNotExistException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Подписки не существует!')

PasswordMismatchException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Пароли не совпадают!')

UnauthorizedException = fastapi.HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверная почта или пароль!')

RefreshTokenMissingException = fastapi.HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Отсутствует токен обновления или он некорректный!')

UserAlreadyDeletedException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Пользователь был удален!')

InvalidTokenException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Некорректный токен или он отсутствует!')

EditForbiddenException = fastapi.HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Изменение не своего желания или категории запрещено!')

QueryMissedException = fastapi.HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Отсутствуют некоторые квери параметры!')

WishAlreadyReservedException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Желание уже было зарезервировано!')

WishNotReservedException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Желание не зарезервировано или зарезервировано не Вами!')

ReserveForbiddenException = fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Нельзя резервировать свое желание!')

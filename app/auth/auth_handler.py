from typing import Annotated
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import Session, select
from app.config import settings
from app.db import get_session
from app.schemas import user as schema_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_password_hash(password):
    """
    Хеширует пароль.

    Args:
        password (str): Пароль.
    Returns:
        str: Хешированная версия пароля.
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """
    Проверяет соответствие пароля его хешу.

    Args:
        plain_password (str): Пароль.
        hashed_password (str): Хешированный пароль.

    Returns:
        bool: True если пароль совпадает с хешем, иначе False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict,
                        expires_delta: timedelta | None = None):
    """
    Создает токен доступа.

    Args:
        data (dict).
        expires_delta (timedelta | None): Время жизни токена

    Returns:
        str: Закодированный токен.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = (datetime.now(timezone.utc) +
                  expires_delta)
    else:
        expire = (datetime.now(timezone.utc) +
                  timedelta(minutes=15))

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,
                             settings.secret_key,
                             algorithm=settings.algo)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                     db_session: Session = Depends(get_session)):
    """
    Получает текущего аутентифицированного пользователя по токену.

    Args:
        token (str): токен.
        db_session (Session): Сессия базы данных.

    Returns:
        UserDb: Объект пользователя из базы данных.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algo])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    statement = (select(schema_user.UserDb)
                 .where(schema_user.UserDb.username == username))
    user = db_session.execute(statement).scalar_one_or_none()

    if user is None:
        raise credentials_exception
    return user

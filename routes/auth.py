from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from schemas import user as schema_user
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from auth import auth_handler
from config import settings
from datetime import timedelta


router = APIRouter(prefix="/auth", tags=["Безопасность"])

@router.post("/signup", status_code=status.HTTP_201_CREATED,
             response_model=int,
             summary = 'Добавить пользователя')
def create_user(user: schema_user.UserModel,
                session: Session = Depends(get_session)):
    new_user = schema_user.UserDb(
        username=user.username,
        email=user.email,
        password=auth_handler.get_password_hash(user.password)
    )
    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user.id
    except IntegrityError as e:
        assert isinstance(e.orig, UniqueViolation)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"User with email {user.email} already exists"
        )


@router.post("/login", status_code=status.HTTP_200_OK,
             summary = 'Войти в систему')
def user_login(login_attempt_data: OAuth2PasswordRequestForm = Depends(),
               db_session: Session = Depends(get_session)):
    statement = (select(schema_user.UserDb)
                 .where(schema_user.UserDb.email == login_attempt_data.username))
    existing_user = db_session.execute(statement).scalar_one_or_none()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User {login_attempt_data.username} not found"
        )

    if auth_handler.verify_password(
            login_attempt_data.password,
            existing_user.password):
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = auth_handler.create_access_token(
            data={"sub": login_attempt_data.username},
            expires_delta=access_token_expires
        )
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Wrong password for user {login_attempt_data.username}"
        )

from datetime import timedelta, date, datetime
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Security
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from core.jwt import decode_token, create_token, refresh_token, save_token, update_user_tokens, delete_old_refresh_token
from core.settings import settings
from src.app.db.db import get_db
from src.base.schemas import Token, RefreshTokenUser, Token_auth
from src.security import get_current_active_superuser

from src.user.models import User as DBUser
from src.user import schemas
from src.user.service import crud_user

from icecream import ic

router = APIRouter()

# TODO: добавить удаление пользователя по id


@router.post("/auth/login", response_model=Token_auth, tags=["auth"])
def auth_user(form_data: schemas.User_auth, db: Session = Depends(get_db)):
    """
    Авторизация пользователя с сохранением jwt токена в БД, если пользователь был авторизован ранее и выполнять
    повторную авторизацию, то мы удаляем старый рефреш токен и создаем новую пару токенов
    :param db: сессия БД
    :param form_data: данные с формы
    :return: токены и их тип
    """
    user = crud_user.authenticate(db, email=form_data.email, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Неверный email или пароль")
    delete_old_refresh_token(db_session=db, user_id=user.id, fingerprint=form_data.fingerprint)

    jwt_refresh = create_token(data={"user_id": user.id, "email": user.email},
                               type_token="refresh")
    jwt_access = create_token(data={"user_id": user.id, "email": user.email},
                              type_token="access")

    save_token(db_session=db, user_id=user.id, refresh_token=jwt_refresh.get("refresh_token_jwt"),
                         fingerprint=form_data.fingerprint,
                         issued=jwt_refresh.get("payload")["iat"], expires=jwt_refresh.get("payload")["exp"])
    return {
        "access_token": jwt_access.get("access_encoded_jwt"),
        "refresh_token": jwt_refresh.get("refresh_token_jwt"),
        "token_type": "bearer",
        "exp": jwt_access.get("payload")["exp"],
        "user_id": jwt_access.get("payload")["user_id"]
    }


@router.put("/auth/refresh_tokens", response_model=Token_auth, tags=["token"])
def update_tokens(old_refresh_token: str, fingerprint: str, db: Session = Depends(get_db)):
    user = crud_user.get_by_token(db, old_refresh_token)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь с данным токеном не найден", )
    if user.fingerprint != fingerprint:
        raise HTTPException(status_code=404, detail="Неверный fingerprint")

    new_tokens = refresh_token(expired_token=old_refresh_token)
    update_user_tokens(db_session=db, user_id=user.user_id, old_refresh_tokens=old_refresh_token,
                            new_refresh_token=new_tokens.get("refresh_token")["refresh_token_jwt"])


    return {
        "access_token": new_tokens["access_token"]["access_encoded_jwt"],
        "refresh_token": new_tokens["refresh_token"]["refresh_token_jwt"],
        "token_type": "bearer",
        "exp": new_tokens["access_token"]["payload"]["exp"],
        "user_id": new_tokens["access_token"]["payload"]["user_id"]
    }


@router.put("/auth/logout", tags=["auth"])
def logout_user():
    pass


@router.get("/get-users", response_model=List[schemas.User], tags=["user-get"])
def get_all_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """
    Получить всех пользователей
    :param db: сессия БД
    :param skip: offset
    :param limit: лимит
    :param current_user: проверка на суперпользователя
    :return:
    """
    return crud_user.get_all_user(db, skip=skip, limit=limit)



@router.get("/get-by-user-id", tags=["user-get"], response_model=schemas.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return crud_user.get_by_user_id(db_session=db, user_id=user_id)


@router.post("/create-user", tags=["user"], response_model=schemas.User)
def create_user(*, db: Session = Depends(get_db), user_in: schemas.User_create):
    """
    Создание пользователя
    :param db: сессия БД
    :param user_in: pydantic модель создания пользователя
    :return:
    """
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует.")
    user = crud_user.create(db, obj_in=user_in)

    return user


@router.put("/update-user", tags=["user"], response_model=schemas.User)
def update_user(*, db: Session = Depends(get_db), user_in: schemas.User_update,
                user_id: int):
    return crud_user.update_by_user_id(db_session=db, obj_in=user_in, user_id=user_id)



@router.get("/decode-token", tags=["token"])
def decode_access_token(token):
    res = decode_token(token)
    return res

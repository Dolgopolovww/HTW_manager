import time
from datetime import datetime, timedelta

from fastapi import HTTPException
from icecream import ic
from jose import jwt
from sqlalchemy.orm import Session

from src.user.models import User_token
from .settings import settings

ALGORITHM = "HS256"


def create_token(*, data: dict, type_token: str):
    """
    Создание токена
    :param data: данные пользователя
    :param type_token: тип создаваемого токена, "access" или "refresh"
    :return: сгенерированный токен пользователя
    """

    expires_delta = timedelta(
        minutes=settings.jwt_access_expiration if type_token == "access" else settings.jwt_refresh_expiration)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    payload = {
        "user_id": data.get("user_id"),
        "email": data.get("email"),
        "exp": expire,
        "iat": datetime.utcnow(),
        "sub": "access" if type_token == "access" else "refresh"
    }
    if type_token == "access":
        access_encoded_jwt = jwt.encode(payload, settings.jwt_secret, settings.jwt_algorithm)
        return {"payload": payload,
                "access_encoded_jwt": access_encoded_jwt}
    else:
        refresh_token_jwt = jwt.encode(payload, settings.jwt_secret, settings.jwt_algorithm)
        return {"payload": payload,
                "refresh_token_jwt": refresh_token_jwt}


def decode_token(token: str):
    """
    Декодирование токена пользователя
    :param token: токен пользователя
    :return: payload если время жизни токена не вышло
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=settings.jwt_algorithm)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Срок действия токена истек")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Недействительный токен")


def refresh_token(expired_token):
    """
    Обновление токена
    :param expired_token: рефреш токен пользователя
    :return: новую пару токенов
    """
    try:
        payload = decode_token(expired_token)
        new_access_token = create_token(data=payload, type_token="access")
        new_refresh_token = create_token(data=payload, type_token="refresh")
        return {"access_token": new_access_token,
                "refresh_token": new_refresh_token}
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Недействительный токен")


def delete_old_refresh_token(db_session: Session, user_id: int, fingerprint: str):
        """
        Удаление старого рефреш токена пользователя, при повторной авторизации.
        :param db_session:
        :param user_id:
        :param fingerprint:
        :return:
        """
        user_refresh_token = db_session.query(User_token).filter(User_token.user_id == user_id,
                                                                 User_token.fingerprint == fingerprint).first()
        if user_refresh_token:
            db_session.delete(user_refresh_token)

def save_token(db_session: Session, user_id: int, refresh_token: str, fingerprint: str, issued: int,
                   expires: int):
        req = User_token(
            user_id=user_id,
            refresh_token=refresh_token,
            fingerprint=fingerprint,
            issued=issued,
            expires_in=expires)
        db_session.add(req)
        db_session.commit()
        db_session.refresh(req)
        return req

def update_user_tokens(db_session: Session, user_id: int, old_refresh_tokens: str, new_refresh_token: str):
        db_session.query(User_token).filter(User_token.user_id == user_id,
                                            User_token.refresh_token == old_refresh_tokens).\
            update({User_token.refresh_token: new_refresh_token})


        db_session.commit()


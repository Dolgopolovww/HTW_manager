from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose.jwt import JWTError
from jose import jwt
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN

from src.app.db.db import get_db
from src.user.service import crud_user

from core.settings import settings
from core.jwt import ALGORITHM
from src.user.models import User
from src.base.schemas import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/user/login/access-token")

def get_current_user(
    db: Session = Depends(get_db), token: str = Security(reusable_oauth2)
):
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except JWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = crud_user.get(db, id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(current_user: User = Security(get_current_user)):
    if not crud_user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(current_user: User = Security(get_current_user)):
    if not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

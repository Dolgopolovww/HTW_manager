from typing import Optional

from icecream import ic
from sqlalchemy.orm import Session

from core.security import verify_password, get_password_hash
from src.base.service import CRUDBase
from src.user.models import User, User_token
from src.user.schemas import User_create, User_update


class CRUDUser(CRUDBase[User, User_create, User_update]):
    def get_by_email(self, db_session: Session, *, email: str) -> Optional[User]:
        return db_session.query(User).filter(User.email == email).first()

    def get_by_user_id(self, db_session: Session, user_id: int) -> Optional[User]:
        res = db_session.query(User).filter(User.id == user_id).first()
        return res

    def get_by_token(self, db_session: Session, refresh_token: str):
        return db_session.query(User_token).filter(User_token.refresh_token == refresh_token).first()

    def is_superuser(self, user: User) -> bool:
        return user.super_user

    def create(self, db_session: Session, *, obj_in: User_create) -> User:
        req = User(email=obj_in.email, password_hash=get_password_hash(obj_in.password))
        db_session.add(req)
        db_session.commit()
        db_session.refresh(req)
        return req

    def update_by_user_id(self, db_session: Session, *, obj_in: User_update, user_id: int) -> Optional[User]:
        db_session.query(User).filter(User.id == user_id).update({
            User.name: obj_in.name, User.surname: obj_in.surname, User.patronymic: obj_in.patronymic,
            User.password_hash: get_password_hash(obj_in.password), User.avatar: obj_in.avatar,
            User.dob: obj_in.dob, User.phone_number: obj_in.phone_number, User.other_contacts: obj_in.other_contacts,
            User.rank: obj_in.rank, User.role: obj_in.role, User.salary: obj_in.salary, User.comments: obj_in.comments,
            User.experience: obj_in.experience})
        db_session.commit()

    def authenticate(self, db_session: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db_session, email=email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def delete_old_refresh_token(self, db_session: Session, user_id: int, fingerprint: str):
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

    def save_token(self, db_session: Session, user_id: int, refresh_token: str, fingerprint: str, issued: int,
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

    def update_tokens(self, db_session: Session, user_id: int, old_refresh_tokens: str, new_refresh_token: str):
        db_session.query(User_token).filter(User_token.user_id == user_id,
                                            User_token.refresh_token == old_refresh_tokens).\
            update({User_token.refresh_token: new_refresh_token})


        db_session.commit()


crud_user = CRUDUser(User)

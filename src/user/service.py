import os
import shutil
import sys
from typing import Optional, List

from fastapi import UploadFile
from icecream import ic
from sqlalchemy.orm import Session

from core.security import verify_password, get_password_hash
from src.base.service import CRUDBase
from src.project.models import Project_team
from src.user import schemas
from src.user.models import User, User_token, User_avatar


class CRUDUser(CRUDBase[schemas.User, schemas.User_create, schemas.User_update]):
    def get_by_email(self, db_session: Session, *, email: str) -> Optional[schemas.User]:
        return db_session.query(User).filter(User.email == email).first()

    def get_user_by_id(self, db_session: Session, user_id: int) -> Optional[schemas.User]:
        return db_session.query(User).filter(User.id == user_id).first()

    def get_users(self, db_session: Session) -> List[Optional[schemas.User]]:
        return db_session.query(User).all()

    def get_by_token(self, db_session: Session, refresh_token: str):
        return db_session.query(User_token).filter(User_token.refresh_token == refresh_token).first()

    def get_free_or_busy_user(self, db_session: Session, flag: bool) -> List[Optional[schemas.User]]:
        return db_session.query(User).filter(User.busy_status == flag).all()

    def is_superuser(self, user: User) -> bool:
        return user.super_user

    def path_validation(self, user_id: int):
        root_dir = os.path.dirname(sys.modules['__main__'].__file__)
        if os.path.exists(f"{root_dir}\\users"):
            pass
        else:
            os.mkdir(f"{root_dir}\\users")
        if os.path.exists(f"{root_dir}\\users\\{user_id}"):
            pass
        else:
            os.mkdir(f"{root_dir}\\users\\{user_id}")
        path_user = f"{root_dir}\\users\\{user_id}\\"
        return path_user

    def create(self, db_session: Session, *, obj_in: schemas.User_create) -> schemas.User_base_in_db:
        user = User(email=obj_in.email, super_user=obj_in.is_superuser,
                    password_hash=get_password_hash(obj_in.password),
                    name=obj_in.name, surname=obj_in.surname, patronymic=obj_in.patronymic, avatar=obj_in.avatar,
                    dob=obj_in.dob, phone_number=obj_in.phone_number, other_contacts=obj_in.other_contacts,
                    rank=obj_in.rank, role=obj_in.role, salary=obj_in.salary, comments=obj_in.comments,
                    competencies=obj_in.competencies, experience=obj_in.experience, busy_status=False)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    def update_by_user_id(self, db_session: Session, *, obj_in: schemas.User_update, user_id: int) -> Optional[
        schemas.User]:
        db_session.query(User).filter(User.id == user_id).update({
            User.email: obj_in.email, User.name: obj_in.name, User.surname: obj_in.surname,
            User.patronymic: obj_in.patronymic,
            User.password_hash: get_password_hash(obj_in.password), User.avatar: obj_in.avatar,
            User.dob: obj_in.dob, User.phone_number: obj_in.phone_number, User.other_contacts: obj_in.other_contacts,
            User.rank: obj_in.rank, User.role: obj_in.role, User.salary: obj_in.salary, User.comments: obj_in.comments,
            User.competencies: obj_in.competencies, User.experience: obj_in.experience})
        db_session.commit()

    def get_avatar_user(self, db_session: Session, user_id: int):
        return db_session.query(User_avatar).filter(User_avatar.user_id == user_id).first()

    def add_avatar_user_by_user_id(self, db_session: Session, user_id: int, avatar: UploadFile, path_user: str):
        try:
            req = User_avatar(user_id=user_id, path_user=path_user, file_name=avatar.filename,
                              content_type=avatar.content_type)
            db_session.add(req)
            db_session.commit()
            with open(f"{path_user}{avatar.filename}", "wb") as buffer:
                shutil.copyfileobj(avatar.file, buffer)
        except Exception as ex:
            ic("add_avatar_user_by_user_id", ex)
            db_session.rollback()

    def delete_avatar_user(self, db_session: Session, user_id: int):
        try:
            avatar_user = db_session.query(User_avatar).filter(User_avatar.user_id == user_id).first()
            db_session.delete(avatar_user)
            db_session.flush()
            os.remove(avatar_user.path_user + avatar_user.file_name)
            db_session.commit()
        except Exception as ex:
            ic("delete_avatar_user", ex)
            db_session.rollback()

    def authenticate(self, db_session: Session, *, email: str, password: str) -> Optional[schemas.User]:
        user = self.get_by_email(db_session, email=email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def delete_user_by_id(self, db_session: Session, user_id: int):
        try:
            self.delete_avatar_user(db_session, user_id)
            db_session.query(Project_team).filter(Project_team.user_id == user_id).delete()
            db_session.flush()
            db_session.query(User).filter(User.id == user_id).delete()
            db_session.commit()
            path_user = self.path_validation(user_id)
            shutil.rmtree(path_user)
        except Exception as ex:
            db_session.rollback()
            ic(ex)


crud_user = CRUDUser(User)

from typing import Optional, List

from icecream import ic
from sqlalchemy.orm import Session

from core.security import verify_password, get_password_hash
from src.base.service import CRUDBase
from src.user.models import User, User_token
from src.user import schemas


class CRUDUser(CRUDBase[schemas.User, schemas.User_create, schemas.User_update]):
    def get_by_email(self, db_session: Session, *, email: str) -> Optional[schemas.User]:
        return db_session.query(User).filter(User.email == email).first()


    def get_by_user_id(self, db_session: Session, user_id: int) -> Optional[schemas.User]:
        return db_session.query(User).filter(User.id == user_id).first()


    def get_all_user(self, db_session: Session, skip=0, limit=100) -> List[Optional[schemas.User]]:
        return db_session.query(User).offset(skip).limit(limit).all()



    def get_by_token(self, db_session: Session, refresh_token: str):
        return db_session.query(User_token).filter(User_token.refresh_token == refresh_token).first()


    def is_superuser(self, user: User) -> bool:
        return user.super_user


    def create(self, db_session: Session, *, obj_in: schemas.User_create) -> schemas.User_base_in_db:
        user = User(email=obj_in.email, super_user=obj_in.is_superuser, password_hash=get_password_hash(obj_in.password),
                    name=obj_in.name, surname=obj_in.surname, patronymic=obj_in.patronymic, avatar=obj_in.avatar,
                    dob=obj_in.dob, phone_number=obj_in.phone_number, other_contacts=obj_in.other_contacts,
                    rank=obj_in.rank, role=obj_in.role, salary=obj_in.salary, comments=obj_in.comments,
                    competencies=obj_in.competencies, experience=obj_in.experience)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    def update_by_user_id(self, db_session: Session, *, obj_in: schemas.User_update, user_id: int) -> Optional[schemas.User]:
        db_session.query(User).filter(User.id == user_id).update({
            User.email: obj_in.email, User.name: obj_in.name, User.surname: obj_in.surname, User.patronymic: obj_in.patronymic,
            User.password_hash: get_password_hash(obj_in.password), User.avatar: obj_in.avatar,
            User.dob: obj_in.dob, User.phone_number: obj_in.phone_number, User.other_contacts: obj_in.other_contacts,
            User.rank: obj_in.rank, User.role: obj_in.role, User.salary: obj_in.salary, User.comments: obj_in.comments,
            User.competencies: obj_in.competencies, User.experience: obj_in.experience})
        db_session.commit()

    def authenticate(self, db_session: Session, *, email: str, password: str) -> Optional[schemas.User]:
        user = self.get_by_email(db_session, email=email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

crud_user = CRUDUser(User)

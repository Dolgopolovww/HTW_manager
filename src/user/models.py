from sqlalchemy import Column, String, Text, Integer, Boolean, ForeignKey, Date, BigInteger
from sqlalchemy.orm import relationship
from src.app.db.db import Base

class User(Base):
    # пользователь
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    surname = Column(String)
    patronymic = Column(String)
    password_hash = Column(Text)
    avatar = Column(String)
    dob = Column(Date)
    phone_number = Column(BigInteger)
    email = Column(String)
    other_contacts = Column(String)
    rank = Column(Integer, ForeignKey('ranks.id'))
    salary = Column(String)
    comments = Column(String)
    competencies = Column(String)
    experience = Column(Date)
    role = Column(Integer, ForeignKey('roles.id'))
    super_user = Column(Boolean)
    busy_status = Column(Boolean)

    user_id_teamlead = relationship("Project")
    user_id_token = relationship("User_token")
    user_id_avatar = relationship("User_avatar")
    user_id_project_team = relationship("Project_team")


class User_token(Base):
    # токен пользователя и данные для него
    __tablename__ = 'user_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    refresh_token = Column(Text)
    fingerprint = Column(Text)
    issued = Column(Integer)  # дата создания токена (1505467152069)
    expires_in = Column(Integer)  # время жизни токена (1505467756869)


class User_avatar(Base):
    __tablename__ = 'user_avatar'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    avatar_path = Column(String)



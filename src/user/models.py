from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from src.project.models import Project, Project_link, Rank, Role

from src.app.db.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    surname = Column(String)
    patronymic = Column(String)
    password_hash = Column(Text)
    avatar = Column(String)
    dob = Column(Date)
    phone_number = Column(Integer)
    email = Column(String)
    other_contacts = Column(String)
    rank = Column(Integer, ForeignKey('ranks.id'))
    salary = Column(String)
    comments = Column(String)
    experience = Column(Date)
    role = Column(Integer, ForeignKey('roles.id'))
    super_user = Column(Boolean)

    teamlead = relationship("Project")
    user_id_project = relationship("User_project")
    user_id_token = relationship("User_token")



class User_project(Base):
    __tablename__ = 'user_projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id_project = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))


class User_token(Base):
    __tablename__ = 'user_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    refresh_token = Column(Text)
    fingerprint = Column(Text)
    issued = Column(Integer)  # дата создания токена (1505467152069)
    expires_in = Column(Integer)  # время жизни токена (1505467756869)



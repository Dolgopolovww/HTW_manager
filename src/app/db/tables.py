from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Rank(Base):
    __tablename__ = 'ranks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)

    rank = relationship("User")


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    role = relationship("User")


class Project_link(Base):
    __tablename__ = 'project links'

    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String)
    description = Column(String)

    project_links = relationship("Project")


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    customer = Column(String)
    time_project_implementation = Column(DateTime)
    description = Column(String)
    path_design_documents = Column(String)
    project_links = Column(Integer, ForeignKey('project links.id'))
    teamlead = Column(Integer, ForeignKey('users.id'))
    status = Column(Boolean)

    project_id = relationship("User_project")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    surname = Column(String)
    patronymic = Column(String)
    password_hash = Column(Text)
    avatar = Column(String)
    dob = Column(DateTime)
    phone_number = Column(Integer)
    email = Column(String)
    other_contacts = Column(String)
    rank = Column(Integer, ForeignKey('ranks.id'))
    salary = Column(String)
    comments = Column(String)
    experience = Column(DateTime)
    role = Column(Integer, ForeignKey('roles.id'))
    super_user = Column(Boolean)

    teamlead = relationship("Project")
    user_id = relationship("User_project")


class User_project(Base):
    __tablename__ = 'user projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)

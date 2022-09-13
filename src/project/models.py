from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship

from src.app.db.db import Base

class Rank(Base):
    # ранг пользователя (стажер, джун, джун+, мид, мид+, сеньор)
    __tablename__ = 'ranks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)

    user_rank = relationship("User")


class Role(Base):
    # роль пользователя (руководитель, сотрудник, админ)
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    user_role = relationship("User")


class Project_link(Base):
    # проектные ссылки
    __tablename__ = 'project_links'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_project = Column(Integer, ForeignKey("projects.id"))
    link = Column(String)
    description = Column(String)


class Project_file(Base):
    # файлы проекта
    __tablename__ = 'project_files'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_project = Column(Integer, ForeignKey("projects.id"))
    path_project = Column(String)
    file_name = Column(String)
    content_type = Column(String)


class Project_team(Base):
    # команда проекта
    __tablename__ = 'project_teams'

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    user_id = Column(Integer, ForeignKey('users.id'))


class Project(Base):
    # проект
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    customer = Column(String)
    project_start = Column(Date)
    project_completion = Column(Date)
    description = Column(String)
    path_design_documents = Column(String)
    team_lead = Column(Integer, ForeignKey('users.id'))
    status = Column(Boolean)

    project_id_links = relationship("Project_link")
    project_id_project_team = relationship("Project_team")

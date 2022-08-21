from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship

from src.app.db.db import Base

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
    __tablename__ = 'project_links'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_project = Column(Integer, ForeignKey("projects.id"))
    link = Column(String)
    description = Column(String)



class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    customer = Column(String)
    time_project_implementation = Column(Date)
    description = Column(String)
    path_design_documents = Column(String)
    teamlead = Column(Integer, ForeignKey('users.id'))
    status = Column(Boolean)

    project_id = relationship("User_project")
    id_project_links = relationship("Project_link")


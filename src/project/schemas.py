from datetime import datetime, date
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel

class Project_base(BaseModel):
    name: str
    customer: str
    project_start: date
    project_completion: date
    description: str
    path_design_documents: str
    team_lead: int


class Project_links(BaseModel):
    link: str
    description: str

class Project_files(BaseModel):
    path_file: str


class Project_create(Project_base):
    team: List[int]


class Project_update(Project_base):
    team: List[int]


class Project_base_in_db(Project_base):
    id: int
    status: bool

    class Config:
        orm_mode = True


class Project_links_in_db(Project_links):
    id: int

    class Config:
        orm_mode = True

class Project_files_in_db(Project_files):
    id: int

    class Config:
        orm_mode = True






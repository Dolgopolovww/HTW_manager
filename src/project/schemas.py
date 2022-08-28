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
    status: bool

class Project_links(BaseModel):
    link: str
    description: str


class Project_create(Project_base):
    team: List[int]


class Project_update(Project_base):
    team: List[int]


class Project_base_in_db(Project_base):
    id: int

    class Config:
        orm_mode = True

class Project_links_in_db(Project_links):
    id: int

    class Config:
        orm_mode = True






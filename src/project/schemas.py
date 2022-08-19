from datetime import datetime, date
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel

class Project_base(BaseModel):
    name: str
    customer: str
    time_project_implementation: date
    description: str
    path_design_documents: str
    teamlead: int
    status: bool

class Project_links(BaseModel):
    link: str
    description: str


class Project_create(Project_base):
    pass


class Project_update(Project_base):
    pass


class Project_base_in_db(Project_base):
    id: int

    class Config:
        orm_mode = True

class Project_links_in_db(Project_links):
    id: int

    class Config:
        orm_mode = True






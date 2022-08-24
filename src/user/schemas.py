from datetime import datetime, date
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class User_auth(BaseModel):
    email: str
    password: str
    fingerprint: str

class User_base(BaseModel):
    email: str
    is_superuser: Optional[bool] = False


class User_base_in_db(User_base):
    id: int = None

    class Config:
        orm_mode = True


class Optional_rank(str, Enum):
    trainee = 1  # стажер
    junior = 2  # джун
    junior_plus = 3  # джун+
    middle = 4  # мидл
    middle_plus = 5  # мидл+
    senior = 6  # сеньор


class Optional_role(str, Enum):
    supervisor = 1  # руководитель
    employee = 2  # сотрудник
    admin = 3  # админ

class User(User_base_in_db):
    name: str
    surname: str
    patronymic: str
    avatar: str
    dob: date
    phone_number: int
    other_contacts: str
    rank: int
    salary: str
    comments: str
    competencies: str
    experience: date
    role: int


class User_create(User_base):
    password: str
    fingerprint: str
    name: str
    surname: str
    patronymic: str
    avatar: str
    dob: date
    phone_number: int
    other_contacts: str
    rank: Optional_rank
    salary: str
    comments: str
    competencies: str
    experience: date
    role: Optional_role


class User_update(User_base):
    name: str
    surname: str
    patronymic: str
    password: str
    avatar: str
    dob: date
    phone_number: int
    other_contacts: str
    rank: Optional_rank
    salary: str
    comments: str
    competencies: str
    experience: date
    role: Optional_role



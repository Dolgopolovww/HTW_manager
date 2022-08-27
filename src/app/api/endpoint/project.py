from datetime import timedelta, date, datetime
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Security, Query
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from core.jwt import decode_token, create_token, refresh_token, save_token, update_user_tokens, delete_old_refresh_token
from core.settings import settings
from src.app.db.db import get_db
from src.base.schemas import Token, RefreshTokenUser, Token_auth
from src.security import get_current_active_superuser

from src.project import models
from src.project import schemas
from src.project.service import crud_project

from icecream import ic

from src.user.service import crud_user

router = APIRouter()

# TODO: при добавлении нового проекта, можно указать путь к документации, нужно решить как это сделать корректно
# TODO: сделать добавление команды проекта
# TODO: сделать запрос на получение команды проекта по id и по имени проекта

@router.post("/create-project", tags=["project"], response_model=schemas.Project_base_in_db)
def create_project(*, db: Session = Depends(get_db), obj_in: schemas.Project_create):
    check_project = crud_project.get_by_project_name(db, obj_in.name)
    if check_project:
        raise HTTPException(status_code=400, detail="Проект с таким именем уже существует.")
    project = crud_project.create(db, obj_in)
    return project




@router.put("/update-project", tags=["project"], response_model=schemas.Project_update)
def update_project(*, db: Session = Depends(get_db), obj_in: schemas.Project_update, project_id: int):
    # TODO: сделать возможность обновления команды проекта
    project = crud_project.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=400, detail=f"Проект с id {project_id} не найден")
    return crud_project.update_by_project_id(db, obj_in, project_id)




@router.get("/get-projects", tags=["project-get"], response_model=List[schemas.Project_base_in_db])
def get_all_projects(*, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud_project.get_multi(db, skip=skip, limit=limit)


@router.get("/get-by-project-id", tags=["project-get"], response_model=schemas.Project_base_in_db)
def get_project_by_id(*, db: Session = Depends(get_db), project_id: int):
    project = crud_project.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=400, detail=f"Проект с id {project_id} не найден")
    return project


@router.get("/get-by-project-name", tags=["project-get"], response_model=schemas.Project_base_in_db)
def get_project_by_name(*, db: Session = Depends(get_db), project_name: str):
    project = crud_project.get_by_project_name(db, project_name)
    if not project:
        raise HTTPException(status_code=400, detail=f"Проект с именем {project_name} не найден")
    return crud_project.get_by_project_name(db, project_name)


@router.get("/get-links-project", tags=["project-get"], response_model=List[schemas.Project_links_in_db])
def get_project_links_by_id(*, db: Session = Depends(get_db), project_id: int):
    return crud_project.get_links_by_id_project(db, project_id)


@router.post("/add-link-project", tags=["project"])
def add_link_project(*, db: Session = Depends(get_db), links: List[schemas.Project_links], project_id: int):
    crud_project.add_links_project(db, links, project_id)


@router.delete("/delete-link-project", tags=["project"])
def delete_link_project(*, db: Session = Depends(get_db), project_id: int, link_id: int):
    crud_project.delete_link(db, project_id, link_id)


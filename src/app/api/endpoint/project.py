import os
import shutil
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Security, Query, File, UploadFile
from icecream import ic

from sqlalchemy.orm import Session

from src.app.db.db import get_db

from src.project import schemas
from src.project.service import crud_project

from src.user.schemas import User
from src.user.service import crud_user

router = APIRouter()

# TODO: сделать возможность сохранения картинок/документов/всякого в папку с проектом, и сохранением в БД, путь до файла и описание



@router.post("/add-project-file")
def add_file(project_name: str, file: List[UploadFile] = File(...)):
    if os.path.exists(f"projects"):
        pass
    else:
        os.mkdir(f"projects")

    if os.path.exists(f"projects/{project_name}"):
        os.listdir(f"projects/{project_name}")
    else:
        os.mkdir(f"projects/{project_name}")

    path = f"projects/{project_name}"
    for i in file:
        with open(f"{path}/{i.filename}", 'wb') as buffer:
            shutil.copyfileobj(i.file, buffer)




@router.post("/create-project", tags=["project"], response_model=schemas.Project_base_in_db)
def create_project(*, db: Session = Depends(get_db), obj_in: schemas.Project_create):
    check_project = crud_project.get_by_project_name(db, obj_in.name)
    if check_project:
        raise HTTPException(status_code=400, detail="Проект с таким именем уже существует.")
    project = crud_project.create(db, obj_in)
    return project


@router.put("/update-project", tags=["project"], response_model=schemas.Project_update)
def update_project(*, db: Session = Depends(get_db), obj_in: schemas.Project_update, project_id: int):
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


@router.get("/get-project-team", tags=["project-get"], response_model=List[User])
def get_team_project(*, db: Session = Depends(get_db), project_id: int):
    project = crud_project.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=400, detail=f"Проект c id {project_id} не найден")
    team_project = crud_project.get_team_project_by_project_id(db, project_id)
    if not team_project:
        raise HTTPException(status_code=400, detail=f"У проекта с id {project_id} не назначена команда")
    return team_project


@router.get("/get-user-projects", tags=["user-get"], response_model=List[schemas.Project_base_in_db])
def get_user_projects_by_id(*, db: Session = Depends(get_db), user_id: int):
    user = crud_user.get_by_user_id(db, user_id)
    if not user:
        raise HTTPException(status_code=400, detail=f"Пользователь c id {user_id} не найден")
    user_projects = crud_project.get_user_project_by_user_id(db, user_id)
    if len(user_projects) == 0:
        raise HTTPException(status_code=400, detail=f"У пользователя нет проектов")
    return user_projects


@router.post("/add-link-project", tags=["project"])
def add_link_project(*, db: Session = Depends(get_db), links: List[schemas.Project_links], project_id: int):
    crud_project.add_links_project(db, links, project_id)


@router.delete("/delete-link-project", tags=["project"])
def delete_link_project(*, db: Session = Depends(get_db), project_id: int, link_id: int):
    crud_project.delete_link(db, project_id, link_id)


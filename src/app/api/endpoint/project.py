from typing import List

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from icecream import ic
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from src.app.db.db import get_db
from src.project import schemas
from src.project.service import crud_project
from src.user.schemas import User
from src.user.service import crud_user

router = APIRouter()

# TODO: переписать сохранение файла, так как, необходимо хранить путь до файла и имя файла в разны


@router.post("/create-project", tags=["project"], response_model=schemas.Project_base_in_db)
def create_project(*, db: Session = Depends(get_db), obj_in: schemas.Project_create):
    check_project = crud_project.get_project_by_name(db, obj_in.name)
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


@router.put("/closing-project", tags=["project"], response_model=schemas.Project_base_in_db)
def closing_project(project_id: int, db: Session = Depends(get_db)):
    project = crud_project.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=400, detail=f"Проект с id {project_id} не найден")
    crud_project.closing_project_by_id(db, project_id)


@router.post("/add-files-project", tags=["project"])
def add_files_project(project_id: int, db: Session = Depends(get_db), files: List[UploadFile] = File(...)):
    check_project = crud_project.get_by_id(db, project_id)
    if not check_project:
        raise HTTPException(status_code=400, detail=f"Нельзя добавить файлы в несуществующий проект")

    path_project = crud_project.path_validation(check_project.name)  # путь до папки проекта
    res = []
    for file in files:
        ic(file.content_type)
        check_file = crud_project.file_validator(db, file.filename)
        if check_file:
            res.append(f"Файл с именем {file.filename} уже существует")
            pass
        else:
            crud_project.add_files_project_by_project_id(db, project_id, file, path_project)
    if len(res) > 0:
        return res


@router.delete("/delete-file-project", tags=["project"])
def delete_file_project(*, db: Session = Depends(get_db), project_id: int, file_id: int):
    crud_project.delete_file_by_project_id(db, project_id, file_id)


@router.get("/get-projects", tags=["project-get"], response_model=List[schemas.Project_base_in_db])
def get_all_projects(*, db: Session = Depends(get_db)):
    return crud_project.get_multi(db)


@router.get("/get-project-by-id", tags=["project-get"], response_model=schemas.Project_base_in_db)
def get_project_by_id(*, db: Session = Depends(get_db), project_id: int):
    project = crud_project.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=400, detail=f"Проект с id {project_id} не найден")
    return project


@router.get("/get-project-by-name", tags=["project-get"], response_model=schemas.Project_base_in_db)
def get_project_by_name(*, db: Session = Depends(get_db), project_name: str):
    project = crud_project.get_project_by_name(db, project_name)
    if not project:
        raise HTTPException(status_code=400, detail=f"Проект с именем {project_name} не найден")
    return project


@router.get("/get-active-projects", tags=["project-get"], response_model=List[schemas.Project_base_in_db])
def get_active_projects(db: Session = Depends(get_db)):
    return crud_project.get_status_projects(db, True)


@router.get("/get-completed-projects", tags=["project-get"], response_model=List[schemas.Project_base_in_db])
def get_completed_projects(db: Session = Depends(get_db)):
    return crud_project.get_status_projects(db, False)


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

@router.get("/get-project-team-lead", tags=["project-get"], response_model=User)
def get_team_lead_project(*, db: Session = Depends(get_db), project_id: int):
    project = crud_project.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=400, detail=f"Проект c id {project_id} не найден")
    team_lead_project = crud_project.get_team_lead_project_by_project_id(db, project_id)
    if not team_lead_project:
        raise HTTPException(status_code=400, detail=f"У проекта с id {project_id} не назначена тимлид")
    return team_lead_project


@router.get("/get-project-file", tags=["project-get"])
def get_project_file(file_id: int, db: Session = Depends(get_db)):
    file = crud_project.get_file_by_id(db, file_id)
    return FileResponse(file.path_project + "/" + file.file_name, media_type=file.content_type, filename=file.file_name)


@router.get("/get-project-files", tags=["project-get"], response_model=List[schemas.Project_files_in_db])
def get_files_project(*, db: Session = Depends(get_db), project_id: int):
    project = crud_project.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=400, detail=f"Проект c id {project_id} не найден")
    files_project = crud_project.get_files_project_by_project_id(db, project_id)
    if not files_project:
        raise HTTPException(status_code=400, detail=f"У проекта c id {project_id} нет добавленных файлов")
    return files_project


@router.get("/get-user-projects", tags=["user-get"], response_model=List[schemas.Project_base_in_db])
def get_user_projects_by_id(*, db: Session = Depends(get_db), user_id: int):
    user = crud_user.get_user_by_id(db, user_id)
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

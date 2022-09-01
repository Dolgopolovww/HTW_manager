from typing import Optional, List

from fastapi import HTTPException
from icecream import ic
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.base.service import CRUDBase
from src.project import models
from src.project import schemas

import src.user.models as models_user
import src.user.schemas as schemas_user


class CRUDProject(CRUDBase):
    def get_by_project_name(self, db_session: Session, project_name: str):
        return db_session.query(models.Project).filter(models.Project.name == project_name).first()


    def get_links_by_id_project(self, db_session: Session, project_id: int) -> Optional[schemas.Project_links_in_db]:
        return db_session.query(models.Project_link).filter(models.Project_link.id_project == project_id).all()


    def get_team_project_by_project_id(self, db_session: Session, project_id: int) -> List[Optional[schemas_user.User]]:
        query = db_session.query(models_user.User).select_from(models.Project_team)\
            .join(models_user.User).filter(models.Project_team.project_id == project_id).all()
        return query


    def get_user_project_by_user_id(self, db_session: Session, user_id: int) -> List["Optional[schemas.Project_base_in_db]"]:
        project = db_session.query(models.Project_team).filter(models.Project_team.user_id == user_id).all()
        user_projects = []
        for i in project:
            user_projects.append(db_session.query(models.Project).filter(models.Project.id == i.project_id).first())
        return user_projects


    def create(self, db_session: Session, obj_in: schemas.Project_create) -> Optional[schemas.Project_base_in_db]:
        try:
            project = models.Project(name=obj_in.name, customer=obj_in.customer,
                                     project_start=obj_in.project_start, project_completion=obj_in.project_completion,
                                     description=obj_in.description, path_design_documents=obj_in.path_design_documents,
                                     team_lead=obj_in.team_lead, status=obj_in.status)
            db_session.add(project)
            db_session.flush()
            project_id = self.get_by_project_name(db_session, obj_in.name)
            for i in obj_in.team:
                team_project = models.Project_team(project_id=project_id.id, user_id=i)
                db_session.add(team_project)
            db_session.commit()
            return project

        except IntegrityError as ex:
            db_session.rollback()
            raise HTTPException(status_code=400, detail=f"id пользователя которого вы хотите добавить в команду не найден\n{ex}")


    def update_by_project_id(self, db_session: Session, obj_in: schemas.Project_update, project_id: int) -> Optional[schemas.Project_update]:
        try:
            db_session.query(models.Project).filter(models.Project.id == project_id).update({
                models.Project.name: obj_in.name, models.Project.customer: obj_in.customer,
                models.Project.project_start: obj_in.project_start,
                models.Project.project_completion: obj_in.project_completion,
                models.Project.description: obj_in.description,
                models.Project.path_design_documents: obj_in.path_design_documents,
                models.Project.team_lead: obj_in.team_lead, models.Project.status: obj_in.status})
            db_session.flush()
            for i in obj_in.team:
                team_project = models.Project_team(project_id=project_id, user_id=i)
                db_session.add(team_project)
            db_session.commit()
            return obj_in
        except IntegrityError as ex:
            db_session.rollback()
            raise HTTPException(status_code=400, detail=f"id пользователя которого вы хотите добавить в команду не найден\n{ex}")


    def add_links_project(self, db_session: Session, obj_in: schemas.Project_links, project_id: int):
        for i in obj_in:
            req = models.Project_link(id_project=project_id, link=i.link, description=i.description)
            db_session.add(req)
            db_session.commit()
            db_session.refresh(req)


    def delete_link(self, db_session: Session, project_id: int, link_id: int):
        req = db_session.query(models.Project_link).filter(models.Project_link.id_project == project_id,
                                                           models.Project_link.id == link_id).first()
        db_session.delete(req)
        db_session.commit()




crud_project = CRUDProject(models.Project)
from typing import Optional

from icecream import ic
from sqlalchemy.orm import Session

from src.base.service import CRUDBase
from src.project import models
from src.project import schemas


class CRUDProject(CRUDBase):
    def get_by_project_name(self, db_session: Session, project_name: str):
        return db_session.query(models.Project).filter(models.Project.name == project_name).first()


    def get_links_by_id_project(self, db_session: Session, project_id: int) -> Optional[schemas.Project_links_in_db]:
        return db_session.query(models.Project_link).filter(models.Project_link.id_project == project_id).all()


    def create(self, db_session: Session, obj_in: schemas.Project_create) -> Optional[schemas.Project_base_in_db]:
        project = models.Project(name=obj_in.name, customer=obj_in.customer,
                                 time_project_implementation=obj_in.time_project_implementation,
                                 description=obj_in.description, path_design_documents=obj_in.path_design_documents,
                                 teamlead=obj_in.teamlead, status=obj_in.status)
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)
        return project

    def update_by_project_id(self, db_session: Session, obj_in: schemas.Project_update, project_id: int) -> Optional[schemas.Project_base_in_db]:
        db_session.query(models.Project).filter(models.Project.id == project_id).update({
            models.Project.name: obj_in.name, models.Project.customer: obj_in.customer,
            models.Project.time_project_implementation: obj_in.time_project_implementation,
            models.Project.description: obj_in.description,
            models.Project.path_design_documents: obj_in.path_design_documents,
            models.Project.teamlead: obj_in.teamlead, models.Project.status: obj_in.status})
        db_session.commit()

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
from sys import prefix

from fastapi import APIRouter
from src.app.api.endpoint import user
from src.app.api.endpoint import project


routers = APIRouter()


routers.include_router(user.router, prefix="/user")
routers.include_router(project.router, prefix="/project")


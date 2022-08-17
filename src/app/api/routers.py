from fastapi import APIRouter
from src.app.api.endpoint import user


routers = APIRouter()


routers.include_router(user.router, prefix="/user")


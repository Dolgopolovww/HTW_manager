
from pprint import pprint

from fastapi import FastAPI
import uvicorn
from starlette.requests import Request
from starlette.responses import Response

from core.settings import settings
from src.app.api.routers import routers

from src.app.db.db import SessionLocal, engine

app = FastAPI(title="HTW_manager")

# TODO: разграничить права доступа, для супер пользователя и обычных пользователей
# TODO: сделать для тестов дешифратор паролей



@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    response = Response('Internal server error', status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

app.include_router(routers)


if __name__ == '__main__':
    uvicorn.run("main:app",
                port=8888,  # settings.server_port,
                host="0.0.0.0",  # settings.server_host,
                reload=True)



from fastapi import FastAPI
import uvicorn
from starlette.requests import Request
from starlette.responses import Response

from core.settings import settings
from src.app.api import router
from src.app.db.db import SessionLocal

app = FastAPI()
app.include_router(router)


@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    response = Response('Internal server error', status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

if __name__ == '__main__':
    uvicorn.run("main:app",
                port=settings.server_port,
                host=settings.server_host,
                reload=True)
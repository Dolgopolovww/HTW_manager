import sys

import psycopg2
from icecream import ic
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request

from core.settings import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{settings.database_password}@{settings.database_host}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


try:
    engine.connect()
except Exception as ex:
    print(f'Некорректные данные для подключения к БД!\n{ex}')



def get_db(request: Request):
    return request.state.db
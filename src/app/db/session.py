from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.settings import settings




engine = create_engine(settings.database_connect, echo=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
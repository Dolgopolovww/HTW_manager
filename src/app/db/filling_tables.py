from sqlalchemy.orm import sessionmaker

from src.app.db.session import engine
from src.app.db.db import Base
from src.user.models import User
from src.project.models import Rank, Role, Project_link, Project

Session = sessionmaker(bind=engine)
session = Session()


roles = ["руководитель", "сотрудник", "админ"]
exists = session.query(Role).filter(Role.name.in_([i for i in roles])).first()
if not exists:
    res = [Role(name=i) for i in roles]
    session.add_all(res)
    session.commit()

ranks = ["стажер", "джун", "джун+", "мид", "мид+", "сеньор"]
exists = session.query(Rank).filter(Rank.name.in_(i for i in ranks)).first()
if not exists:
    res = [Rank(name=i) for i in ranks]
    session.add_all(res)
    session.commit()
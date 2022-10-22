from sqlmodel import Session, create_engine

from cvm.config import settings
from cvm import models


name = settings.database.name
user = settings.database.user
password = settings.database.password
host = settings.database.host
port = settings.database.port
options = settings.database.options

uri = f"postgresql+psycopg2://{user}:{password}@{host}/{name}?sslmode=disable"

engine = create_engine(uri, echo=False, connect_args={'options': options})
models.SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)

from sqlmodel import Session, create_engine

from cvm.config import settings
from cvm import models

name = settings.database.name
user = settings.database.user
password = settings.database.password
host = settings.database.host
port = settings.database.port
options = settings.database.options


try:
    uri = f"postgresql+psycopg2://{user}:{password}@{host}/{name}?sslmode=disable"
    engine = create_engine(uri, echo=False, connect_args={'options': options})
    models.SQLModel.metadata.create_all(engine)
except Exception as e:
    print("Error[cvm.database]: Erro ao abrir conexão com banco de dados")
    print(str(e))


def get_session() -> Session:
    return Session(engine)
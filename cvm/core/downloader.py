import zipfile
import requests

from datetime import datetime
from typing import Optional,List,Union
from datetime import datetime
from io import BytesIO
from from_root import from_root
from sqlmodel import select

from cvm.database import get_session
from cvm.models import Downloader


TODAY = datetime.now()
YEAR_PRESENT = TODAY.year
DOWNLOAD_PATH = from_root('downloads', mkdirs=True)


def get_last_download_date() -> Union[bool,datetime]:
    with get_session() as session:
        stmt = select(Downloader)
        results = session.exec(stmt).all()
        if len(results) == 0:
            return False
        return results[-1].created_at


def register_download() -> None:
    """"""
    update_date = Downloader(message="OK", success=True)
    with get_session() as session:
        session.add(update_date)
        session.commit()


def downloading() -> None:
    """"""
    print("Iniciando download dos arquivos")
    for y in range(YEAR_PRESENT, YEAR_PRESENT -5, -1):
        url = f"https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/itr_cia_aberta_{y}.zip"
        try: 
            file_name = url.split("/")[-1]
            print(f"Baixando: {file_name}...", end="")
            filebytes = BytesIO(requests.get(url).content)
            filezip = zipfile.ZipFile(filebytes)
            filezip.extractall(f"{DOWNLOAD_PATH}/{y}")
            print(f"salvo com sucesso no diretório: {DOWNLOAD_PATH}/{y}")
        except Exception as e:
            print(f" Opss... algo deu errado ao baixar arquivos!\n{e}")

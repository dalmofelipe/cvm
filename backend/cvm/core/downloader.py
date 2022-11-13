import zipfile
import requests

from datetime import datetime
from datetime import datetime
from io import BytesIO
from from_root import from_root
from sqlmodel import select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

from cvm.database import get_session
from cvm.models import Downloader
from cvm.core.cia_aberta import validate_year_range


TODAY = datetime.now()
CURRENT_YEAR = TODAY.year
DOWNLOAD_PATH = from_root('backend','downloads', mkdirs=True)


def get_last_download_date_from_database() -> datetime | None:
    """
    """
    with get_session() as session:
        stmt = select(Downloader)
        results = session.exec(stmt).all()
        if len(results) == 0:
            return None
        return results[-1].created_at


def register_download() -> None:
    """
    """
    update_date = Downloader(message="OK", success=True)
    with get_session() as session:
        session.add(update_date)
        session.commit()


def download_all_years() -> None:
    """
    Baixa todos ITRs dos ultimos 5 anos
    """
    print("Iniciando download dos arquivos")
    for y in range(CURRENT_YEAR, CURRENT_YEAR -5, -1):
        url = f"https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/itr_cia_aberta_{y}.zip"
        try: 
            file_name = url.split("/")[-1]
            print(f"Baixando: {file_name}... ", end="")
            filebytes = BytesIO(requests.get(url).content)
            filezip = zipfile.ZipFile(filebytes)
            filezip.extractall(f"{DOWNLOAD_PATH}/{y}")
            register_download()
            print(f"OK \U0001F5F8")
        except Exception as e:
            print(f"\U0001F5F4\nError[download_all_years]: Erro ao baixar arquivos\n{e}")


def download_by_year(
    year:int
):
    """
    Baixa ITR de um ano específico
    """
    if validate_year_range(year):
        url = f"https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/itr_cia_aberta_{year}.zip"
        try: 
            file_name = url.split("/")[-1]
            print(f"Baixando: {file_name}... ", end="")
            filebytes = BytesIO(requests.get(url).content)
            filezip = zipfile.ZipFile(filebytes)
            filezip.extractall(f"{DOWNLOAD_PATH}/{year}")
            register_download()
            print(f"OK \U0001F5F8")
            # print(f"ITR-{year}: '{file_name}' salvo com sucesso no diretório: {DOWNLOAD_PATH}/{year}")
        except Exception as e:
            print(f"\U0001F5F4\nError[download_by_year]: Erro ao baixar arquivos\n{e}")

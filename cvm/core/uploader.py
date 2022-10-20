from genericpath import isdir
import os
from time import sleep
import psycopg2

from cvm.config import settings
from from_root import from_root
from cvm.core.downloader import TODAY
from cvm.models import CiaAberta


conn = psycopg2.connect(
    database=settings.database.name, 
    user=settings.database.user, 
    password=settings.database.password, 
    host=settings.database.host, 
    port=settings.database.port,
    options=settings.database.options,
)
conn.autocommit = True
cursor = conn.cursor()


year = TODAY.year
download_folder = from_root('downloads')


def exec_query_upload(year):
    """"""
    doc_name = f"itr_cia_aberta_{year}.csv"
    path = f"{download_folder}/{year}"
    file_path = f"{path}/{doc_name}"
    table_name = CiaAberta.__tablename__
    schema = settings.database.name 

    if os.path.isdir(path) and os.path.isfile(file_path):
        query = f"""COPY {schema}.{table_name}(cnpj_cia,dt_refer,versao,denom_cia,cd_cvm,categ_doc,id_doc,dt_receb,link_doc)\
 FROM '{path}/{doc_name}'\
 DELIMITER ';'\
 CSV HEADER;"""

        #print(query)
        try:
            cursor.execute(query)
            print(f"Upload do arquivo [{doc_name}] realizado com sucesso!")
        except Exception as e:
            print(f"Erro[exec_query_upload]\nErro ao processar query de upload dos dados!\n{e}")
    else:
        print(f"Erro[exec_query_upload]\nArquivo não encontrado: {file_path}")


def upload_itr_cia_aberta():
    for y in range(year -4, year +1, 1):
        exec_query_upload(y)
        sleep(2)


upload_itr_cia_aberta()

conn.commit()
conn.close()
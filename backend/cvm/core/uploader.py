import os
import psycopg2

from time import sleep
from datetime import datetime
from from_root import from_root
from sqlmodel import select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

from cvm.config import settings
from cvm.core.downloader import TODAY
from cvm.database import get_session
from cvm.models import (CiaAberta, CiaAbertaBPAInd, CiaAbertaBPPCon, CiaAbertaBPPInd, 
    CiaAbertaDFCMDCon, CiaAbertaDFCMDInd, CiaAbertaDFCMICon, CiaAbertaDFCMIInd, 
    CiaAbertaDMPLCon, CiaAbertaDMPLInd, CiaAbertaDRACon, CiaAbertaDRAInd, CiaAbertaDRECon, 
    CiaAbertaDREInd, CiaAbertaDVACon, CiaAbertaDVAInd, Uploader, CiaAbertaBPACon)


try:
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
except Exception as e:
    print("Error[cvm.core.upload]: Error ao abrir conexão com banco de dados")
    print(str(e))


CURRENT_YEAR = TODAY.year
DOWNLOAD_FOLDER = from_root('backend','downloads')
DOWNLOAD_FOLDER_PG_DOCKER="/downloads"  # bind com a pasta no container do postgres
SCHEMA = settings.database.schema
HEADER_PATTERN = {
    "INFO": "cnpj_cia,dt_refer,versao,denom_cia,cd_cvm,categ_doc,id_doc,dt_receb,link_doc",
    "BASE": "cnpj_cia,dt_refer,versao,denom_cia,cd_cvm,grupo_dfp,moeda,escala_moeda,ordem_exerc,dt_fim_exerc,cd_conta,ds_conta,vl_conta,st_conta_fixa",
    "DMLP": "cnpj_cia,dt_refer,versao,denom_cia,cd_cvm,grupo_dfp,moeda,escala_moeda,ordem_exerc,dt_ini_exerc,dt_fim_exerc,coluna_df,cd_conta,ds_conta,vl_conta,st_conta_fixa",
    "DFC": "cnpj_cia,dt_refer,versao,denom_cia,cd_cvm,grupo_dfp,moeda,escala_moeda,ordem_exerc,dt_ini_exerc,dt_fim_exerc,cd_conta,ds_conta,vl_conta,st_conta_fixa"
}
CSV_INFO = [
    { "file": 'itr_cia_aberta_', "table": CiaAberta.__tablename__, "header": HEADER_PATTERN['INFO'] }, 
    { "file": 'itr_cia_aberta_BPA_con_', "table": CiaAbertaBPACon.__tablename__, "header": HEADER_PATTERN['BASE'] }, 
    { "file": 'itr_cia_aberta_BPA_ind_', "table": CiaAbertaBPAInd.__tablename__, "header": HEADER_PATTERN['BASE'] }, 
    { "file": 'itr_cia_aberta_BPP_con_', "table": CiaAbertaBPPCon.__tablename__, "header": HEADER_PATTERN['BASE'] }, 
    { "file": 'itr_cia_aberta_BPP_ind_', "table": CiaAbertaBPPInd.__tablename__, "header": HEADER_PATTERN['BASE'] }, 
    { "file": 'itr_cia_aberta_DFC_MD_con_', "table": CiaAbertaDFCMDCon.__tablename__, "header": HEADER_PATTERN['DFC'] }, 
    { "file": 'itr_cia_aberta_DFC_MD_ind_', "table": CiaAbertaDFCMDInd.__tablename__, "header": HEADER_PATTERN['DFC'] }, 
    { "file": 'itr_cia_aberta_DFC_MI_con_', "table": CiaAbertaDFCMICon.__tablename__, "header": HEADER_PATTERN['DFC'] }, 
    { "file": 'itr_cia_aberta_DFC_MI_ind_', "table": CiaAbertaDFCMIInd.__tablename__, "header": HEADER_PATTERN['DFC'] }, 
    { "file": 'itr_cia_aberta_DMPL_con_', "table": CiaAbertaDMPLCon.__tablename__, "header": HEADER_PATTERN['DMLP'] }, 
    { "file": 'itr_cia_aberta_DMPL_ind_', "table": CiaAbertaDMPLInd.__tablename__, "header": HEADER_PATTERN['DMLP'] }, 
    { "file": 'itr_cia_aberta_DRA_con_', "table": CiaAbertaDRACon.__tablename__, "header": HEADER_PATTERN['DFC'] }, 
    { "file": 'itr_cia_aberta_DRA_ind_', "table": CiaAbertaDRAInd.__tablename__, "header": HEADER_PATTERN['DFC'] }, 
    { "file": 'itr_cia_aberta_DRE_con_', "table": CiaAbertaDRECon.__tablename__, "header": HEADER_PATTERN['DFC'] }, 
    { "file": 'itr_cia_aberta_DRE_ind_', "table": CiaAbertaDREInd.__tablename__, "header": HEADER_PATTERN['DFC'] }, 
    { "file": 'itr_cia_aberta_DVA_con_', "table": CiaAbertaDVACon.__tablename__, "header": HEADER_PATTERN['DFC'] }, 
    { "file": 'itr_cia_aberta_DVA_ind_', "table": CiaAbertaDVAInd.__tablename__, "header": HEADER_PATTERN['DFC'] }
]


def get_last_upload_date() -> datetime | None:
    with get_session() as session:
        stmt = select(Uploader).order_by(Uploader.created_at).limit(1)
        results = session.exec(stmt).all()
        if len(results) <= 0: return None
        return results[0].created_at


def register_upload() -> None:
    """
    """
    update_date = Uploader(message="OK", success=True)
    with get_session() as session:
        session.add(update_date)
        session.commit()


def exec_query_upload(year):
    """
    """
    flag_error = False # mudar isso, urgente

    for doc in CSV_INFO:
        doc_name = f"{doc['file']}{year}.csv"
        path = f"{DOWNLOAD_FOLDER}/{year}"
        doc_path = f"{path}/{doc_name}"
        table_name = doc['table']
        header = doc['header']

        if os.path.isdir(path) and os.path.isfile(doc_path):
            query = f"""COPY {SCHEMA}.{table_name}({header})\
 FROM '{DOWNLOAD_FOLDER_PG_DOCKER}/{year}/{doc_name}'\
 WITH DELIMITER ';'\
 NULL AS E\'\'\
 CSV HEADER ENCODING 'latin-1';"""

            try:
                print(f"Upload do arquivo [{doc_name}]... ", end="")
                cursor.execute(query)
                sleep(1)
                print(f"OK \U0001F5F8")
            except Exception as e:
                print(f"\U0001F5F4\nErro[exec_query_upload]: Erro ao processar query de upload dos dados!")
                print(f"Arquivo:{doc_name}\nTabela:{doc['table']}\nErro:{e}")
        else:
            print(f"Erro[exec_query_upload]: Arquivo ou diretório não encontrado: \n{doc_path}")
            print(f"verifique se a pasta '{path}' foi criada pelo comando 'cvm download' ")
            flag_error = True
            break

    if not flag_error:
        register_upload()
    
    conn.commit()
    conn.close()

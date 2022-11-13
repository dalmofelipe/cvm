import shutil
import typer
import subprocess

from typing import Optional
from datetime import timedelta

from cvm.core.downloader import (TODAY, DOWNLOAD_PATH, download_all_years, download_by_year,
    get_last_download_date_from_database)
from cvm.core.uploader import exec_query_upload, get_last_upload_date


main = typer.Typer(help="API REST para os dados abertos da Comissão de Valores Mobiliários")


@main.command('download')
def download(
    year:int = TODAY.year, 
    all:Optional[bool] = False
):
    """Baixa demonstrativos trimestraias ITR direto da CVM.\
Serão salvos na raiz do projeto na pasta donwloads"""
    last = get_last_download_date_from_database()
    if last and  TODAY.__sub__(last) < timedelta(days=7):
        print(f"já foi realizado o download essa semana no dia {last}")
        return
    if all:
        download_all_years()
    else:
        download_by_year(year)


@main.command('remove')
def remove_download_folder():
    """Exclui a pasta downloads da raiz do projeto.\
Use apos realizar o upload dos dados para o bando de dados."""
    shutil.rmtree(DOWNLOAD_PATH)


@main.command('upload')
def database_upload(
    year:int
):
    """
    Sobe os dados dos arquivos CSVs da pasta download para o banco de dados
    """
    last = get_last_upload_date()
    if last and TODAY.__sub__(last) < timedelta(days=7):
        print(f"já foi realizado o upload essa semana no dia {last}")
        return
    exec_query_upload(year)


@main.command("api")
def run_api(
    port:int = 8000
):
    """Inicia API Rest em localhost"""
    # uvicorn cvm.api.main:app --reload --port 8000
    subprocess.run(["uvicorn", "cvm.api.main:app", "--reload", '--port', str(port)])

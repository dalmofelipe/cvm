from datetime import timedelta
import typer

from cvm.core.downloader import TODAY, downloading, get_last_download_date, register_download


main = typer.Typer(help="API Rest da Comissão de Valores Mobiliários")


@main.command('download')
def download():
    """Baixa os arquivos da cvm, salvando na pasta donwloads na raiz do projeto\n\
        ..."""
    # verifica a ultima data de download
    last = get_last_download_date()
    if last and TODAY.__sub__(last)  < timedelta(days=7):
        print(f"já foi realizado o download essa semana no dia {last}")
        return
    # registra nova data caso for maior que sete dias. os são atualizados semanalmente
    register_download()
    # remove pasta anterior
    # dowload dos arquivos, a pasta "download" será criada na raiz do projeto
    downloading()


@main.command('validate')
def download_dir_validate():
    """valida a estrutura da pasta download se esta viavel para upload dos dados"""
    print('download dir ok...')
    pass


@main.command('upload')
def database_upload():
    """Sobe os dados dos arquivos CSVs da pasta download para o banco de dados"""
    print('upload ok...')
    pass

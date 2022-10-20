from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Downloader(SQLModel, table=True):

    __tablename__ : str  = 'tb_downloads'

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    message:str
    success:bool = Field(default=False)


class CiaAberta(SQLModel, table=True):
    
    __tablename__ : str  = 'tb_cia_aberta'

    id: Optional[int] = Field(default=None, primary_key=True)
    cnpj_cia : str
    dt_refer : datetime = Field(default_factory=datetime.now)
    versao : int
    denom_cia : str
    cd_cvm : str
    categ_doc : str
    id_doc : str
    dt_receb : datetime = Field(default_factory=datetime.now)
    link_doc : str

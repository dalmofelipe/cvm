from datetime import datetime
from sys import flags
from typing import Optional
from sqlmodel import Field, SQLModel


class Downloader(SQLModel, table=True):

    __tablename__ : str  = 'tb_downloads'

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    message:str
    success:bool = Field(default=False)


class Uploader(SQLModel, table=True):

    __tablename__ : str  = 'tb_uploads'

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    message:str
    success:bool = Field(default=False)


class CiaAberta(SQLModel, table=True):
    
    __tablename__ : str  = 'tb_cia_aberta'

    id: Optional[int] = Field(default=None, primary_key=True)
    cnpj_cia : str
    dt_refer : datetime
    versao : int
    denom_cia : str
    cd_cvm : str
    categ_doc : str
    id_doc : str
    dt_receb : datetime
    link_doc : str


class CiaBaseModel(SQLModel):
    
    id: Optional[int] = Field(default=None, primary_key=True)
    cnpj_cia: str
    dt_refer: datetime
    versao: int
    denom_cia: str
    cd_cvm: str
    grupo_dfp: str
    moeda: str
    escala_moeda: str
    ordem_exerc: str
    dt_fim_exerc: datetime
    cd_conta: str
    ds_conta: str = Field(nullable=True)
    vl_conta: float
    st_conta_fixa: str


# Balanço Patrimonial Ativo (BPA)
class CiaAbertaBPACon(CiaBaseModel, table=True):
    
    __tablename__ : str  = 'tb_cia_aberta_bpa_con'


# 
class CiaAbertaBPAInd(CiaBaseModel, table=True):
    
    __tablename__ : str  = 'tb_cia_aberta_bpa_ind'


# Balanço Patrimonial Passivo (BPP)
class CiaAbertaBPPCon(CiaBaseModel, table=True):
    
    __tablename__ : str  = 'tb_cia_aberta_bpp_con'

 
class CiaAbertaBPPInd(CiaBaseModel, table=True):
    
    __tablename__ : str  = 'tb_cia_aberta_bpp_ind'


# Demonstração de Fluxo de Caixa - Método Direto (DFC-MD)
class CiaAbertaDFCMDCon(CiaBaseModel, table=True):
    
    __tablename__ : str  = 'tb_cia_aberta_dfc_md_con'

    dt_ini_exerc: datetime


class CiaAbertaDFCMDInd(CiaBaseModel, table=True):
    
    __tablename__ : str  = 'tb_cia_aberta_dfc_md_ind'

    dt_ini_exerc: datetime


# Demonstração de Fluxo de Caixa - Método Indireto (DFC-MI)
class CiaAbertaDFCMICon(CiaBaseModel, table=True):
    
    __tablename__ : str  = 'tb_cia_aberta_dfc_mi_con'

    dt_ini_exerc: datetime


class CiaAbertaDFCMIInd(CiaBaseModel, table=True):
    
    __tablename__ : str  = 'tb_cia_aberta_dfc_mi_ind'

    dt_ini_exerc: datetime


# Demonstração das Mutações do Patrimônio Líquido (DMPL)
class CiaAbertaDMPLCon(CiaBaseModel, table=True):
    
    __tablename__ : str  = 'tb_cia_aberta_dmpl_con'

    dt_ini_exerc: datetime
    coluna_df: str = Field(nullable=True)


class CiaAbertaDMPLInd(CiaBaseModel, table=True):
    
    __tablename__ : str  = 'tb_cia_aberta_dmpl_ind'

    dt_ini_exerc: datetime
    coluna_df: str = Field(nullable=True)


# Demonstração de Resultado Abrangente (DRA)
class CiaAbertaDRACon(CiaBaseModel, table=True):
    
    __tablename__ : str  = 'tb_cia_aberta_dra_con'

    dt_ini_exerc: datetime


class CiaAbertaDRAInd(CiaBaseModel, table=True):
    
    __tablename__ : str  = 'tb_cia_aberta_dra_int'

    dt_ini_exerc: datetime


# Demonstração de Resultado (DRE)
class CiaAbertaDRECon(CiaBaseModel, table=True):
    
    __tablename__ : str  = 'tb_cia_aberta_dre_con'

    dt_ini_exerc: datetime


class CiaAbertaDREInd(CiaBaseModel, table=True):
    
    __tablename__ : str  = 'tb_cia_aberta_dre_ind'

    dt_ini_exerc: datetime


# Demonstração de Valor Adicionado (DVA)
class CiaAbertaDVACon(CiaBaseModel, table=True):
    
    __tablename__ : str  = 'tb_cia_aberta_dva_con'

    dt_ini_exerc: datetime


class CiaAbertaDVAInd(CiaBaseModel, table=True):
    
    __tablename__ : str  = 'tb_cia_aberta_dva_ind'

    dt_ini_exerc: datetime

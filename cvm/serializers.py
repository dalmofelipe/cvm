from pydantic import BaseModel
from datetime import datetime 



class CiaAbertaOut(BaseModel):
    id: int
    cnpj_cia : str
    # dt_refer : datetime
    versao : int
    denom_cia : str
    cd_cvm : str
    categ_doc : str
    id_doc : str
    dt_receb : datetime
    link_doc : str

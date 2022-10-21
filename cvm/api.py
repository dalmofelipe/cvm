from fastapi import FastAPI
from typing import List, Optional

from cvm.core.cia_aberta import (
    get_all_cia_aberta_from_db,
    get_by_id_cia_aberta_from_db,
    get_by_name_cia_aberta_from_db
)
from cvm.serializers import CiaAbertaOut


# uvicorn cvm.api:api --reload
api = FastAPI(title="API REST CVM")


@api.get("/cia-aberta", response_model=List[CiaAbertaOut])
async def show_all_cia_aberta(
    name: Optional[str] = None,
    limit: Optional[int] = 10,
    page: Optional[int] = 1
)   -> List[CiaAbertaOut]: 
    """Lista CIAs e suas informções básicas de cadastro"""
    if name:
        return get_by_name_cia_aberta_from_db(name, limit, page)
    return get_all_cia_aberta_from_db(limit, page)


@api.get("/cia-aberta/{cia_id:int}", response_model=CiaAbertaOut)
async def search_by_name_cia_aberta(
    cia_id:int
) -> CiaAbertaOut:
    return get_by_id_cia_aberta_from_db(cia_id)

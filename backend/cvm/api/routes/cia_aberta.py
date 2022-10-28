from pydoc import describe
from fastapi import APIRouter
from typing import List, Optional

from cvm.core.cia_aberta import (
    get_by_id_cia_aberta_from_db,
    get_by_filters_cia_aberta_from_db
)
from cvm.serializers import CiaAbertaOut


routes = APIRouter(
    prefix="/cia-aberta",
    tags=["cia-aberta"]
)


@routes.get(
    "/", 
    response_model=List[CiaAbertaOut],
)
async def show_by_filters_cia_aberta(
    name: Optional[str] = None,
    limit: Optional[int] = 10,
    page: Optional[int] = 1
)   -> List[CiaAbertaOut]: 
    """Lista CIAs e suas informções básicas de cadastro"""
    return get_by_filters_cia_aberta_from_db(name, limit, page)


@routes.get(
    "/{cia_id:int}", 
    response_model=CiaAbertaOut,
    responses = { 404: { 'description': 'informe um ID dentro de um interválo válido' }}
)
async def show_by_id_cia_aberta(
    cia_id:int
) -> CiaAbertaOut:
    """CiaAbertaOut"""
    return get_by_id_cia_aberta_from_db(cia_id)

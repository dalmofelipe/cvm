from typing import List
from sqlmodel import select, text

from cvm.database import get_session
from cvm.models import CiaAberta
from cvm.serializers import CiaAbertaOut


def get_all_cia_aberta_from_db(
    limit:int = 10, 
    page:int = 0
) -> List[CiaAbertaOut]:
    if page <= 0 or limit <= 0:
        return []

    offset:int = (page * limit) - limit 

    with get_session() as session:
        query = select(CiaAberta)
        query = query.offset(offset).limit(limit)
        return list(session.exec(query))


def get_by_id_cia_aberta_from_db(id:int) -> CiaAbertaOut:
    with get_session() as session:
        query = select(CiaAberta) 
        query = query.where(CiaAberta.id == id)
        result = session.exec(query)
        return result.first()


def get_by_name_cia_aberta_from_db(
    name:str, 
    limit:int = 10, 
    page:int = 0
) -> List[CiaAbertaOut]:
    if page <= 0 or limit <= 0:
        return []

    offset = (page * limit) - limit 

    with get_session() as session:
        query = select(CiaAberta).offset(offset).limit(limit)\
            .where(text(f"denom_cia like '%{name.upper()}%'"))
        result = session.exec(query).all()
        return result

from typing import List, Optional
from sqlmodel import select, text
from datetime import datetime

from cvm.database import get_session
from cvm.models import CiaAberta
from cvm.serializers import CiaAbertaOut


TODAY = datetime.now()
CURRENT_YEAR = TODAY.year


def get_by_id_cia_aberta_from_db(id:int) -> CiaAbertaOut:
    with get_session() as session:
        query = select(CiaAberta).where(CiaAberta.id == id)
        return session.exec(query).first()


def get_by_filters_cia_aberta_from_db(
    name: Optional[str], 
    limit: int = 10, 
    page: int = 0
) -> List[CiaAbertaOut]:
    if page <= 0 or limit <= 0:
        return []

    offset = (page * limit) - limit 

    with get_session() as session:
        query = select(CiaAberta).offset(offset).limit(limit)
        if name:
            query = query.where(text(f"denom_cia like '%{name.upper()}%'"))
        return session.exec(query).all()



def validate_year_range(year:int) -> bool:
    min_year = CURRENT_YEAR -5
    max_year = CURRENT_YEAR
    if year < min_year or year > max_year:
        print(f"Error[validate_year_range]: Informe um ano entre {min_year} e {max_year}")
        return False
    return True

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.term import Term
from app.schemas.term import TermResponse, TermSchema
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()

router = APIRouter(prefix="/v1/term")


@router.post("/add_many", status_code=status.HTTP_201_CREATED)
async def create_multi_term(payload: list[TermSchema], db_session: AsyncSession = Depends(get_db)):
    try:
        term_instances = [Term(**term.model_dump()) for term in payload]
        db_session.add_all(term_instances)
        await db_session.commit()
    except SQLAlchemyError as ex:
        # logger.exception(ex)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)) from ex
    else:
        logger.info(f"{len(term_instances)} instances of term inserted into database.")
        return True


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TermResponse)
async def create_term(payload: TermSchema, db_session: AsyncSession = Depends(get_db)):
    term = Term(**payload.model_dump())
    await term.save(db_session)
    return term


@router.get("/{name}", response_model=TermResponse)
async def find_term(
    name: str,
    db_session: AsyncSession = Depends(get_db),
):
    return await Term.find(db_session, name)


@router.delete("/{name}")
async def delete_term(name: str, db_session: AsyncSession = Depends(get_db)):
    term = await Term.find(db_session, name)
    return await term.delete(term, db_session)


@router.patch("/{name}", response_model=TermResponse)
async def update_term(
    payload: TermSchema,
    name: str,
    db_session: AsyncSession = Depends(get_db),
):
    term = await Term.find(db_session, name)
    await term.update(db_session, **payload.model_dump())
    return term

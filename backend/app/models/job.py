import uuid

from fastapi import HTTPException, status
from sqlalchemy import String, select, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, Mapped

from app.models.base import Base


class Job(Base):
    __tablename__ = "job"
    __table_args__ = ({"schema": "default"},)
    id: Mapped[uuid:UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4, autoincrement=True)
    status: Mapped[str] = mapped_column(String)
    date_started: Mapped[str | None] = mapped_column(DateTime)


    @classmethod
    async def get(cls, db_session: AsyncSession, id: UUID):
        """

        :param db_session:
        :param id:
        :return:
        """
        stmt = select(cls).where(cls.id == id)
        result = await db_session.execute(stmt)
        instance = result.scalars().first()
        if instance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"Record not found": f"There is no record for requested id: {id}"},
            )
        else:
            return instance


    # @classmethod
    # async def find(cls, db_session: AsyncSession, name: str):
    #     """
    #
    #     :param db_session:
    #     :param name:
    #     :return:
    #     """
    #     stmt = select(cls).where(cls.name == name)
    #     result = await db_session.execute(stmt)
    #     instance = result.scalars().first()
    #     if instance is None:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail={"Record not found": f"There is no record for requested name value : {name}"},
    #         )
    #     else:
    #         return instance

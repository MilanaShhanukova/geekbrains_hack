import uuid

from fastapi import HTTPException, status
from sqlalchemy import String, select, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, Mapped

from app.models.base import Base


class Term(Base):
    __tablename__ = "term"
    __table_args__ = ({"schema": "default"},)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    definition: Mapped[str | None] = mapped_column(Text)

    @classmethod
    async def find(cls, db_session: AsyncSession, name: str):
        """

        :param db_session:
        :param name:
        :return:
        """
        stmt = select(cls).where(cls.name == name)
        result = await db_session.execute(stmt)
        instance = result.scalars().first()
        if instance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"Not found": f"There is no record for name: {name}"},
            )
        else:
            return instance

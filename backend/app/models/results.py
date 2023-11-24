import uuid

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.models.base import Base


class WhisperResult(Base):
    __tablename__ = "whisper_result"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.id", ondelete='CASCADE'))
    job = relationship("Job", back_populates="whisper_result", uselist=False)
    text: Mapped[str | None] = mapped_column(Text)


class LLMResult(Base):
    __tablename__ = "llm_result"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.id", ondelete='CASCADE'))
    job = relationship("Job", back_populates="llm_result", uselist=False)
    text: Mapped[str | None] = mapped_column(Text)


class ParserResult(Base):
    __tablename__ = "parser_result"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.id", ondelete='CASCADE'))
    job = relationship("Job", back_populates="parser_result", uselist=False)
    text: Mapped[str | None] = mapped_column(Text)

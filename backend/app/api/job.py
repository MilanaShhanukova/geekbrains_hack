from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.job import Job
from app.schemas.job import JobResponse, JobSchema

router = APIRouter(prefix="/v1/job")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=JobResponse)
async def create_job(payload: JobSchema, db_session: AsyncSession = Depends(get_db)):
    nonsense = Job(**payload.model_dump())
    await nonsense.save(db_session)
    # celery_app
    return nonsense


# @router.get("/", response_model=JobResponse)
# async def find_job(
#     name: str,
#     db_session: AsyncSession = Depends(get_db),
# ):
#     return await Job.find(db_session, name)


@router.delete("/")
async def delete_job(job_id: UUID, db_session: AsyncSession = Depends(get_db)):
    job = await Job.get(db_session, job_id)
    return await job.delete(job, db_session)


@router.patch("/", response_model=JobResponse)
async def update_job(
    payload: JobSchema,
    job_id: UUID,
    db_session: AsyncSession = Depends(get_db),
):
    job = await Job.get(db_session, job_id)
    await job.update(db_session, **payload.model_dump())
    return job


@router.post("/", response_model=JobResponse)
async def merge_job(
    payload: JobSchema,
    db_session: AsyncSession = Depends(get_db),
):
    job = Job(**payload.model_dump())
    await job.save_or_update(db_session)
    return job

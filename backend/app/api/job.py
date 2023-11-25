from uuid import UUID

from celery import chain
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.celery import celery_app
from app.database import get_db
from app.models.job import Job
from app.schemas.job import JobResponse, JobSchema, JobResultResponse
from app.services.auth import AuthBearer

from fastapi import UploadFile


router = APIRouter(prefix="/v1/job", tags=["JOB, Bearer"], dependencies=[Depends(AuthBearer())])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=JobResponse)
async def create_job(audio_file: UploadFile, db_session: AsyncSession = Depends(get_db)):
    job = Job(status="created",
              audio_file=audio_file)
    await job.save(db_session)
    chain_of_tasks = chain(
        f'worker.tasks.tasks.whisper_task.s({job.id})',
        f'worker.tasks.tasks.get_result.s({job.id})'
    )

    result = chain_of_tasks.apply_async()
    return job

@router.get("/status", status_code=status.HTTP_200_OK, response_model=JobResponse)
async def get_job_status(job_id: UUID, db_session: AsyncSession = Depends(get_db)):
    job = await Job.get(db_session, job_id)
    return job


@router.get("/result", status_code=status.HTTP_200_OK, response_model=JobResultResponse)
async def get_job_result(job_id: UUID, db_session: AsyncSession = Depends(get_db)):
    job = await Job.get(db_session, job_id)
    r = JobResultResponse(
        id=job.id,
        status=job.status,
        result=job.keywords_result.keywords
    )
    return r


# @router.get("/", response_model=JobResponse)
# async def find_job(
#     name: str,
#     db_session: AsyncSession = Depends(get_db),
# ):
#     return await Job.find(db_session, name)

@router.get("/")
async def get_job(job_id: UUID, db_session: AsyncSession = Depends(get_db)):
    job = await Job.get(db_session, job_id)
    return job


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


# @router.post("/", response_model=JobResponse)
# async def merge_job(
#     payload: JobSchema,
#     db_session: AsyncSession = Depends(get_db),
# ):
#     job = Job(**payload.model_dump())
#     await job.save_or_update(db_session)
#     return job

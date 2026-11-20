"""Job progress for polling from the UI."""

import uuid

from fastapi import APIRouter, HTTPException, status

from app.api.deps import DbSession
from app.api.schemas import JobOut
from app.db.models import Job

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: uuid.UUID, db: DbSession) -> Job:
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job not found")
    return job

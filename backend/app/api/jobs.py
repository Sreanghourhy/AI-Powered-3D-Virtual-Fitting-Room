"""Job progress for polling from the UI (owner only)."""

import uuid

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, DbSession
from app.api.schemas import JobOut
from app.db.models import Job

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: uuid.UUID, user: CurrentUser, db: DbSession) -> Job:
    job = db.get(Job, job_id)
    if job is None or job.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job not found")
    return job

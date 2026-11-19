"""Create background jobs. Processing happens in app.worker."""

import uuid

from sqlalchemy.orm import Session

from app.db.models import Job


def enqueue(
    db: Session,
    *,
    user_id: uuid.UUID,
    job_type: str,
    ref_id: str | None = None,
    payload: dict | None = None,
) -> Job:
    job = Job(user_id=user_id, type=job_type, ref_id=ref_id, payload=payload or {})
    db.add(job)
    db.flush()
    return job

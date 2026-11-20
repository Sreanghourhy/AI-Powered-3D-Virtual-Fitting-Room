"""Create background jobs. Processing happens in app.worker."""

from sqlalchemy.orm import Session

from app.db.models import Job


def enqueue(
    db: Session,
    *,
    job_type: str,
    ref_id: str | None = None,
    payload: dict | None = None,
) -> Job:
    job = Job(type=job_type, ref_id=ref_id, payload=payload or {})
    db.add(job)
    db.flush()
    return job

"""Database-backed job worker: ``python -m app.worker``.

Picks the oldest queued job, runs its handler, records progress and the result.
Runs one job at a time to protect the MacBook (docs/02-architecture.md, D4).
"""

import logging
import signal
import time
from datetime import UTC, datetime

from sqlalchemy import select, update

from app.db.models import Job
from app.db.session import session_factory
from app.worker.handlers import HANDLERS, JobContext, JobError

log = logging.getLogger("worker")

GENERIC_ERROR = "Something went wrong while processing. Please try again."


def claim_next() -> Job | None:
    """Atomically move the oldest queued job to 'processing' and return it."""
    with session_factory()() as db:
        oldest = (
            select(Job.id).where(Job.status == "queued").order_by(Job.created_at).limit(1)
        ).scalar_subquery()
        job_id = db.execute(
            update(Job)
            .where(Job.id == oldest, Job.status == "queued")
            .values(status="processing", started_at=datetime.now(UTC), progress=0)
            .returning(Job.id)
        ).scalar_one_or_none()
        db.commit()
        return db.get(Job, job_id) if job_id else None


def _set(job_id, **values) -> None:  # noqa: ANN001, ANN003
    with session_factory()() as db:
        db.execute(update(Job).where(Job.id == job_id).values(**values))
        db.commit()


def run_job(job: Job) -> None:
    def report(progress: int, step: str | None = None) -> None:
        _set(job.id, progress=max(0, min(100, int(progress))), step=step)

    func = HANDLERS.get(job.type)
    try:
        if func is None:
            raise JobError(f"Unknown job type: {job.type}")
        func(JobContext(job=job, report=report))
    except JobError as exc:
        log.warning("Job %s failed: %s", job.id, exc)
        _set(job.id, status="failed", error=str(exc)[:500], finished_at=datetime.now(UTC))
    except Exception:
        # Full details go to the server log only; the customer sees a generic message.
        log.exception("Job %s crashed", job.id)
        _set(job.id, status="failed", error=GENERIC_ERROR, finished_at=datetime.now(UTC))
    else:
        _set(job.id, status="done", progress=100, step=None, finished_at=datetime.now(UTC))


def run_once() -> bool:
    """Process one job if available. Returns True if a job was processed."""
    job = claim_next()
    if job is None:
        return False
    log.info("Running job %s (%s)", job.id, job.type)
    run_job(job)
    return True


def fail_interrupted_jobs() -> int:
    """Jobs left 'processing' by a crashed/stopped worker are marked failed on startup."""
    with session_factory()() as db:
        result = db.execute(
            update(Job)
            .where(Job.status == "processing")
            .values(
                status="failed",
                error="Processing was interrupted. Please try again.",
                finished_at=datetime.now(UTC),
            )
        )
        db.commit()
        return result.rowcount or 0


def main(poll_seconds: float = 1.0) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    stopping = False

    def stop(*_args: object) -> None:
        nonlocal stopping
        stopping = True
        log.info("Stopping after the current job…")

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    if count := fail_interrupted_jobs():
        log.warning("Marked %d interrupted job(s) as failed", count)
    log.info("Worker started. Handlers: %s", ", ".join(sorted(HANDLERS)))
    while not stopping:
        if not run_once():
            time.sleep(poll_seconds)

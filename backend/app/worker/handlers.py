"""Job handlers. Register with @handler("type"). Real reconstruction comes in Phase 4."""

import time
from collections.abc import Callable
from dataclasses import dataclass

from app.db.models import Job


class JobError(Exception):
    """Expected failure. The message is shown to the customer, so keep it plain and safe."""


@dataclass
class JobContext:
    job: Job
    report: Callable[[int, str | None], None]  # (progress 0-100, step name)


Handler = Callable[[JobContext], None]
HANDLERS: dict[str, Handler] = {}


def handler(job_type: str) -> Callable[[Handler], Handler]:
    def register(func: Handler) -> Handler:
        HANDLERS[job_type] = func
        return func

    return register


@handler("sleep")
def sleep_job(ctx: JobContext) -> None:
    """Dummy job for testing the pipeline: sleeps in steps and reports progress."""
    steps = int(ctx.job.payload.get("steps", 4))
    delay = float(ctx.job.payload.get("delay", 0.5))
    for i in range(1, steps + 1):
        time.sleep(delay)
        ctx.report(round(i * 100 / steps), f"step {i} of {steps}")

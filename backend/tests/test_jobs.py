import uuid

import pytest
from fastapi.testclient import TestClient

from app.db.models import Job
from app.db.session import session_factory
from app.services.jobs import enqueue
from app.worker import handlers
from app.worker.runner import GENERIC_ERROR, claim_next, fail_interrupted_jobs, run_once
from tests.helpers import signup


def _enqueue(user_id: str, job_type: str = "sleep", **payload: object) -> str:
    with session_factory()() as db:
        job = enqueue(db, user_id=uuid.UUID(user_id), job_type=job_type, payload=payload)
        db.commit()
        return str(job.id)


def test_new_job_is_queued(client: TestClient) -> None:
    user = signup(client)
    job_id = _enqueue(user["id"], steps=2, delay=0)
    body = client.get(f"/jobs/{job_id}").json()
    assert body["status"] == "queued"
    assert body["progress"] == 0


def test_sleep_job_runs_to_done(client: TestClient) -> None:
    user = signup(client)
    job_id = _enqueue(user["id"], steps=4, delay=0)
    assert run_once() is True
    body = client.get(f"/jobs/{job_id}").json()
    assert body["status"] == "done"
    assert body["progress"] == 100
    assert body["startedAt"] and body["finishedAt"]
    assert run_once() is False  # queue empty


def test_progress_visible_while_processing(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    user = signup(client)
    seen: list[dict] = []

    def probe(ctx: handlers.JobContext) -> None:
        ctx.report(40, "reconstructing")
        seen.append(client.get(f"/jobs/{ctx.job.id}").json())

    monkeypatch.setitem(handlers.HANDLERS, "probe", probe)
    _enqueue(user["id"], job_type="probe")
    run_once()
    assert seen[0]["status"] == "processing"
    assert seen[0]["progress"] == 40
    assert seen[0]["step"] == "reconstructing"


def test_job_error_message_shown(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    user = signup(client)

    def bad(ctx: handlers.JobContext) -> None:
        raise handlers.JobError("Not enough back views were matched.")

    monkeypatch.setitem(handlers.HANDLERS, "bad", bad)
    job_id = _enqueue(user["id"], job_type="bad")
    run_once()
    body = client.get(f"/jobs/{job_id}").json()
    assert body["status"] == "failed"
    assert body["error"] == "Not enough back views were matched."


def test_crash_hides_internal_details(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    user = signup(client)

    def crash(ctx: handlers.JobContext) -> None:
        raise RuntimeError("/Users/secret/path/scan.jpg exploded")

    monkeypatch.setitem(handlers.HANDLERS, "crash", crash)
    job_id = _enqueue(user["id"], job_type="crash")
    run_once()
    body = client.get(f"/jobs/{job_id}").json()
    assert body["status"] == "failed"
    assert body["error"] == GENERIC_ERROR


def test_unknown_job_type_fails(client: TestClient) -> None:
    user = signup(client)
    job_id = _enqueue(user["id"], job_type="does-not-exist")
    run_once()
    assert client.get(f"/jobs/{job_id}").json()["status"] == "failed"


def test_jobs_run_oldest_first_and_claimed_once(client: TestClient) -> None:
    user = signup(client)
    first = _enqueue(user["id"], steps=1, delay=0)
    _enqueue(user["id"], steps=1, delay=0)
    claimed = claim_next()
    assert str(claimed.id) == first
    assert str(claim_next().id) != first  # the first job can't be claimed twice


def test_interrupted_jobs_marked_failed(client: TestClient) -> None:
    user = signup(client)
    job_id = _enqueue(user["id"])
    claim_next()  # now "processing", as if the worker died mid-job
    assert fail_interrupted_jobs() == 1
    assert client.get(f"/jobs/{job_id}").json()["status"] == "failed"


def test_job_requires_login(client: TestClient) -> None:
    user = signup(client)
    job_id = _enqueue(user["id"])
    client.cookies.clear()
    assert client.get(f"/jobs/{job_id}").status_code == 401


def test_other_users_job_is_404(client: TestClient) -> None:
    alice = signup(client, "alice@example.com")
    job_id = _enqueue(alice["id"])
    client.cookies.clear()
    signup(client, "bob@example.com")
    assert client.get(f"/jobs/{job_id}").status_code == 404


def test_deleting_user_deletes_jobs(client: TestClient) -> None:
    from app.db.models import User

    alice = signup(client)
    _enqueue(alice["id"])
    with session_factory()() as db:
        db.delete(db.get(User, uuid.UUID(alice["id"])))
        db.commit()
        assert db.query(Job).count() == 0

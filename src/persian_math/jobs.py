from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from time import monotonic
from uuid import uuid4


class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


@dataclass(frozen=True)
class Job:
    job_id: str
    kind: str
    payload: dict[str, str]
    status: JobStatus = JobStatus.QUEUED
    attempts: int = 0
    created_at: float = 0.0


@dataclass(frozen=True)
class JobPolicy:
    timeout_seconds: float = 30.0
    max_attempts: int = 3
    max_queue: int = 100


_DEFAULT_POLICY = JobPolicy()


class InMemoryJobQueue:
    def __init__(self, policy: JobPolicy | None = None) -> None:
        self.policy = policy or _DEFAULT_POLICY
        self._jobs: dict[str, Job] = {}

    def enqueue(self, kind: str, payload: dict[str, str]) -> Job:
        if len(self._jobs) >= self.policy.max_queue:
            raise RuntimeError("queue limit reached")
        if not kind.strip():
            raise ValueError("job kind required")
        job = Job(uuid4().hex, kind, dict(payload), created_at=monotonic())
        self._jobs[job.job_id] = job
        return job

    def claim(self, job_id: str) -> Job:
        job = self._jobs[job_id]
        if job.status != JobStatus.QUEUED:
            raise ValueError("job is not claimable")
        claimed = Job(
            job.job_id,
            job.kind,
            job.payload,
            JobStatus.RUNNING,
            job.attempts + 1,
            job.created_at,
        )
        self._jobs[job_id] = claimed
        return claimed

    def finish(self, job_id: str, success: bool) -> Job:
        job = self._jobs[job_id]
        status = (
            JobStatus.SUCCEEDED
            if success
            else JobStatus.FAILED
            if job.attempts >= self.policy.max_attempts
            else JobStatus.QUEUED
        )
        updated = Job(job.job_id, job.kind, job.payload, status, job.attempts, job.created_at)
        self._jobs[job_id] = updated
        return updated

    def cancel(self, job_id: str) -> Job:
        job = self._jobs[job_id]
        updated = Job(
            job.job_id, job.kind, job.payload, JobStatus.CANCELLED, job.attempts, job.created_at
        )
        self._jobs[job_id] = updated
        return updated

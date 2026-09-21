from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProductionConfig:
    environment: str
    log_level: str = "INFO"
    max_request_bytes: int = 20 * 1024 * 1024
    worker_timeout_seconds: int = 30
    graceful_shutdown_seconds: int = 15


@dataclass(frozen=True)
class RecoveryPlan:
    backup_required: bool = True
    rollback_supported: bool = True
    restore_verification_required: bool = True


def validate_config(config: ProductionConfig) -> None:
    if config.environment not in {"local", "test", "staging", "production"}:
        raise ValueError("invalid environment")
    if config.max_request_bytes <= 0 or config.worker_timeout_seconds <= 0:
        raise ValueError("invalid resource limits")
    if config.graceful_shutdown_seconds <= 0:
        raise ValueError("invalid shutdown timeout")


def validate_recovery(plan: RecoveryPlan) -> None:
    if not plan.backup_required or not plan.rollback_supported or not plan.restore_verification_required:
        raise ValueError("production recovery controls are incomplete")

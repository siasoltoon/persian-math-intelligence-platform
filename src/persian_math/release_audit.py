from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AuditItem:
    name: str
    passed: bool
    evidence: str


@dataclass(frozen=True)
class ReleaseAudit:
    items: tuple[AuditItem, ...]

    @property
    def passed(self) -> bool:
        return bool(self.items) and all(item.passed for item in self.items)

    @property
    def blockers(self) -> tuple[AuditItem, ...]:
        return tuple(item for item in self.items if not item.passed)


REQUIRED_AREAS = (
    "architecture",
    "mathematics",
    "verification",
    "ocr",
    "security",
    "reliability",
    "performance",
    "tests",
    "ux",
    "deployment",
    "recovery",
    "documentation",
)


def build_audit(evidence: dict[str, bool]) -> ReleaseAudit:
    items = tuple(
        AuditItem(area, bool(evidence.get(area, False)), "evidence_recorded")
        for area in REQUIRED_AREAS
    )
    return ReleaseAudit(items)

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Any


@dataclass(frozen=True)
class Metric:
    name: str
    value: float
    tags: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class Span:
    name: str
    duration_ms: float
    success: bool


class Metrics:
    def __init__(self) -> None:
        self._items: list[Metric] = []

    def observe(self, name: str, value: float, **tags: str) -> None:
        self._items.append(Metric(name, float(value), tuple(sorted(tags.items()))))

    def snapshot(self) -> tuple[Metric, ...]:
        return tuple(self._items)


def timed(name: str):
    def decorator(func: Any):
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            start = perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                _ = Span(name, (perf_counter() - start) * 1000.0, True)
        return wrapped
    return decorator

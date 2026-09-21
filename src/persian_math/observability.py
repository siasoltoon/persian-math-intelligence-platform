from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Any, Callable, TypeVar


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


F = TypeVar("F", bound=Callable[..., Any])


def timed(name: str, recorder: list[Span] | None = None) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            start = perf_counter()
            success = False
            try:
                result = func(*args, **kwargs)
                success = True
                return result
            finally:
                if recorder is not None:
                    recorder.append(Span(name, (perf_counter() - start) * 1000.0, success))
        return wrapped  # type: ignore[return-value]
    return decorator

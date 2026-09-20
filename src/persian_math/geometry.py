from __future__ import annotations

from dataclasses import dataclass
from math import hypot


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class Segment:
    start: Point
    end: Point

    @property
    def length(self) -> float:
        return hypot(self.end.x - self.start.x, self.end.y - self.start.y)


@dataclass(frozen=True)
class Triangle:
    a: Point
    b: Point
    c: Point


@dataclass(frozen=True)
class GeometryResult:
    value: float
    method: str
    verified: bool


def distance(a: Point, b: Point) -> GeometryResult:
    return GeometryResult(hypot(b.x - a.x, b.y - a.y), "euclidean_distance", True)


def triangle_area(triangle: Triangle) -> GeometryResult:
    value = abs(
        triangle.a.x * (triangle.b.y - triangle.c.y)
        + triangle.b.x * (triangle.c.y - triangle.a.y)
        + triangle.c.x * (triangle.a.y - triangle.b.y)
    ) / 2
    return GeometryResult(value, "shoelace_area", True)


def triangle_is_degenerate(triangle: Triangle) -> bool:
    return triangle_area(triangle).value == 0
